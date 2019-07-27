# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ProgressTracker is a one stop shop for providing progress information and event
counts during time consuming operations performed in command line scripts and Django
management commands.

By wrapping a program in ProgressTracker context managers, a tree of Trackers is
created. Progress is tracked and logged individually for each tracker in the tree, or
specific branches.
 
If the number of iterations that will be performed in a part of the command is known,
the tracker is able to provide an item counter, the percentage completed and the
estimated time left until the tracker is completed.

If the number of iterations to be performed is not known, the tracker provides a count
of items completed and the wall time the tracker has been active so far.

In both cases, the tracker can also be used for counting errors and other notable events
that may occur during processing. Events are automatically associated with their trackers
and event counts are tracked also after the trackers that triggered them are complete.

All events that have occurred since the program was started and the current progress
information for all active trackers is shown at regularly, by default once per
second.

The tracker checks if enough time has passed that another update should be logged each
time the main program interacts with the tracker by start or ending a tracker, starting a
new step on a tracker, or registering an event. So it's beneficial track subtasks, since it
gives the tracker more opportunities to provide timely updates.

If there is nothing to track in a part of a program, the tracker has a function that, if
called, will simply log another update if enough time has passed.

In the following example, progress information is added to a script that processes a
list of tasks, with each main task having a subtask that also processes a list of
subtasks.

.. code-block:: python

    with d1_common.utils.progress_tracker.ProgressTracker(logger) as progress:
        total_main_tasks = 1000
        with progress.tracker("Main task", total_main_tasks) as main_tracker:

            for i in range(total_main_tasks):
                # Tell ProgressTracker that we're working on the next step of the main task.
                main_tracker.step()

                # Tracking a subtask
                sub_task_item_count = random.randint(0, 20)
                with main_tracker.tracker("Subtask", sub_task_item_count) as sub_tracker:
                    sub_tracker.step()

                    # Count some random events for the main task.
                    if random.random() > 0.9:
                        main_tracker.event("An event")

                    # Simulate some random Count some random events for the subtask.
                    if random.random() > 0.95:
                        sub_task.event("Download error", "Specific informmation about the error goes here")

                    time.sleep(0.01)

This yields output such as :
 
.. code-block:: bash

    Main task / Subtask: Extra information to log
    Main task / Subtask: Extra information to log
    Progress:
      Main task: progress: 179/1000 (17.90%), eta: 11.17 sec, dhm: 0d00h00m, runtime: 2.01 sec, 0d00h00m
      Main task / Subtask: progress: 1/6 (16.67%), eta: 0.03 sec, dhm: 0d00h00m, runtime: 0.01 sec, 0d00h00m
    Events
      Main task / Subtask: An event occurred on the subtask: 11
      Main task: An event: 14
    Main task / Subtask: Extra information to log
    Main task / Subtask: Extra information to log
    Progress:
      Main task: progress: 213/1000 (21.30%), eta: 11.16 sec, dhm: 0d00h00m, runtime: 2.39 sec, 0d00h00m
      Main task / Subtask: progress: 1/9 (11.11%), eta: 0.05 sec, dhm: 0d00h00m, runtime: 0.01 sec, 0d00h00m
    Events
      Main task / Subtask: An event occurred on the subtask: 13
      Main task: An event: 20
"""

import logging
import sys
import time

import d1_common.util
import d1_common.utils.ulog


class ProgressTracker:
    def __init__(self, logger=None, log_interval_sec=1.0, log_suppress_sec=3.0):
        """Context manager that is the root of the tree of Trackers.

        Args:
            logger to use:
                Passing this is optional but output looks tidier if ProgressTracker
                uses the same logger as the main program.

            log_interval_sec: float seconds
                Minimal time between writing log entries. Log entries may be written
                with less time between entries if the total processing time for a task
                type is less than the interval, or if processing multiple task types
                concurrently.

            log_suppress_sec: float seconds
                Suppress logging for very short lived tasks.

                Unconditionally logging the progress of a large number of short lived
                tasks floods the log with unhelpful messages.

                This setting suppresses any progress updates from tasks that have been
                active for less time than the set number of seconds. If a task stops
                before that point, it will not be have generated any progress update log
                records. Any events triggered by the task will still be counted and
                included in the event counts.
        """
        self._logger = logger or logging.getLogger(__name__)
        self._log_interval_sec = log_interval_sec
        self._log_suppress_sec = log_suppress_sec
        self._last_log_time = time.time()
        self._root_tracker = Tracker(self, [], None, log_suppress_sec)
        self._event_dict = {}

    # Private

    def __enter__(self):
        return self._root_tracker

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log_progress()

    def _log_progress_at_interval(self):
        """Log a progress update if more time than the specified update interval has
        passed.

        Called implicitly from the Tracker functions. Can be called directly if no Tracker
        based interaction is required by the main program.
        """
        if time.time() >= self._last_log_time + self._log_interval_sec:
            self._log_progress()

    def _log_progress(self):
        """Immediately log a progress update. Called by trackers at completion, in order to
        provide a final, 100% update. Can be called directly if required.
        """
        self._log_events()
        progress_list = self._root_tracker.get_progress()
        if progress_list:
            self._log([], "Progress:")
            for progress_str in progress_list:
                self._log([], progress_str, indent=2)
        self._last_log_time = time.time()

    def _count_event(
        self, path_list, event_name, log_str=None, count_int=1, is_error=False
    ):
        if path_list:
            event_key = " / ".join(path_list) + ": " + event_name
        else:
            event_key = event_name
        self._event_dict.setdefault(event_key, 0)
        self._event_dict[event_key] += count_int
        if log_str:
            log_func = self._logger.error if is_error else self._logger.debug
            self._log(path_list, "{}: {}".format(event_name, log_str), 0, log_func)

    def _log_events(self):
        if self._event_dict:
            self._log([], "Events")
        for event_str, count_int in sorted(self._event_dict.items()):
            self._log([], "{}: {}".format(event_str, count_int), indent=2)

    def _log(self, path_list, msg_str, indent=0, log_func=None):
        if msg_str is None:  # or self._is_cancelled:
            return
        logger = log_func or self._logger.info
        for line in msg_str.splitlines():
            path_str = " / ".join(path_list)
            section_list = []
            if path_str:
                section_list.append(path_str)
            if line.strip():
                section_list.append(line)
            logger(" " * indent + ": ".join(section_list).strip())


# noinspection PyProtectedMember
class Tracker(object):
    def __init__(
        self, root, path_list, total_expected_steps=None, log_suppress_sec=None
    ):
        self._root = root
        self._total_expected_steps = total_expected_steps
        self._log_suppress_sec = log_suppress_sec
        self._child_dict = {}
        self._start_ts = time.time()
        self._is_completed = False
        self._current_step = 0
        self._path_list = path_list
        self._is_completed = False

    def __enter__(self):
        self._root._log_progress_at_interval()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Don't log progress for trackers that are being stopped due to stack being unwound
        # by an exception.
        if exc_type is None:
            self.completed()

    def completed(self):
        """If not using the tracker as a context manager, call when the program is done with the
        tracker to generate a final, 100% update for the part of the program tracked by this
        tracker.
        """
        self._root._log_progress()
        self._is_completed = True

    def tracker(self, tracker_name, total_expected_steps=None, log_suppress_sec=None):
        """Create a new child tracker to track progress in a part of a program, such as a time
        consuming method.

        Args:
            tracker_name: str
                A brief descriptive name for the task being performed.

            total_expected_steps: int
                The number of steps / iterations that will be performed by the task.

                Providing this number enables the tracker to provide an item counter,
                the percentage completed and the estimated time left until the task is
                completed.

                If this value is not provided, the tracker provides number of items
                completed and current wall time consumed by the task.

            log_suppress_sec:
                Override the default log_suppress_sec value set in the root ProgressTracker.
                
                If a new value is provided, it is used for this tracker and becomes the
                new default for all child trackers in this branch.
                
                See the description in ProgressTracker for more information.

        """
        self._child_dict[tracker_name] = Tracker(
            self._root,
            self._path_list + [tracker_name],
            total_expected_steps,
            log_suppress_sec or self._log_suppress_sec,
        )
        return self._child_dict[tracker_name]

    def step(self, current_task_index=None, total_expected_steps=None):
        """Call when starting the next step / iteration of the task.

        Typically called as the first line of code in the inner scope being iterated.

        Args:
            current_task_index (int):
                If the task processing loop may skip or repeat tasks, providing the
                current index of the processing loop here allows the tracker to stay
                synchronized with the task. This parameter can normally be left unset.

            total_expected_steps: int
                Set or update the number of steps in this task.

                Typically, this value is set when creating the tracker, but sometimes
                the number of steps is not known when creating the tracker or it
                changes during processing. In such cases, it can be updated here.

                See ``tracker()`` for more information about the setting.
        """
        self._current_step = current_task_index or self._current_step + 1
        self._total_expected_steps = total_expected_steps or self._total_expected_steps
        self._root._log_progress_at_interval()

    def event(self, event_name, log_str=None, count_int=1, is_error=False):
        """Count an event.

        If a notable event occurs while processing a task, call this function to record
        record the event and, optionally, directly write a log line containing the event
        name and additional information.

        Args:
            event_name: str
                A brief name for the event that occurred. Used as a key in the event
                dict. The same name will also be used in the summary. Don't include
                detailed information in the name, as it will cause the events to be seen
                as different events.

            log_str: str
                Optional message with details about the events. The message is
                immediately written to the log along with the name of the task and a
                path to its position in the Tracker tree.

                While the ``event_name`` doubles as a key and must remain the same for
                the same type of event, ``log_str`` may change between calls.

            count_int:
                Increase the count for the event by more than one.

            is_error: bool
                When True, causes the log records written as a result of the call to
                this method to be written with log.error() instead of log.info().
        """
        self._root._count_event(
            self._path_list, event_name, log_str, count_int, is_error
        )
        self._root._log_progress_at_interval()

    def progress(self):
        """Log current progress if more time than the configured update interval has
        passed.

        The update interval can be set in `log_interval_sec` when the ProgressTracker is
        created. If not set, it falls back to a default of 1 update per second.

        The other methods in this class call this function implicitly. This function can
        be called to ensure progress updates in parts of the program that don't interact
        with the tracker via any of the other methods.
        """
        self._root._log_progress_at_interval()

    def get_progress(self):
        """Return a list of progress strings for all tasks in the branch starting at
        this node.

        It's typically not necessary for programs to call this method directly.
        """
        progress_str = self._get_progress()
        progress_list = [progress_str] if progress_str else []
        # In Python 3.7, sets and dict keys keeping their insertion order became an
        # official language feature, so for 3.7, we log tasks in the order in which
        # the were created. For older, we sort alphabetically.
        child_list = reversed(list(self._child_dict.items()))
        if sys.version_info < (3, 7):
            child_list = sorted(child_list)
        for tracker_name, tracker_obj in child_list:
            progress_list.extend(tracker_obj.get_progress())
        return progress_list

    # Private

    def _get_progress(self):
        """Create a string describing current progress for this task."""
        # Suppress for the root tracker, if it has children.
        if self._child_dict:
            return

        # Suppress for tracker after context manager exit or call to completed().
        if self._is_completed:
            return

        # Suppress for tasks that have not yet lived long enough to yield useful
        # progress information.
        if self._get_tracker_age_sec() < self._log_suppress_sec:
            return

        elapsed_sec = time.time() - self._start_ts
        progress_list = []

        if self._total_expected_steps:
            completed_percent = (
                float(self._current_step) / float(self._total_expected_steps) * 100.0
            )
            completed_percent_str = f"{completed_percent:.2f}%"
            progress_list.append(
                f"progress: {self._current_step}/{self._total_expected_steps} ({completed_percent_str})"
            )
            eta_sec = (elapsed_sec / float(self._current_step + 1)) * float(
                self._total_expected_steps - self._current_step
            )
            progress_list.append(f"eta: {self._format_sec(eta_sec)}")

        elif self._current_step:
            progress_list.append(f"step: {self._current_step}")

        progress_list.append(
            f"runtime: {self._format_sec(time.time() - self._start_ts)}"
        )

        return f"{' / '.join(self._path_list)}: {', '.join(progress_list)}"

    def _format_sec(self, sec):
        if sec < 3 * 60:
            return f"{sec:.2f} sec"
        if sec < 24 * 60 * 60:
            return d1_common.util.format_sec_to_hms(sec)
        else:
            return d1_common.util.format_sec_to_dhm(sec)

    def _get_tracker_age_sec(self):
        return time.time() - self._start_ts
