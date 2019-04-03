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

"""One stop shop for providing progress information and event counts during time
consuming operations performed in command line scripts and Django management commands.

The ProgressLogger keeps track of how many tasks have been processed by a script, how
many are remaining, and how much time has been used. It then calculates and periodically
displays a progress update containing an ETA and completed percentage.

The ProgressLogger can also be used for counting errors and other notable events that
may occur during processing, and displays total count for each type of tracked event in
the progress updates.

In the following example, progress information is added to a script that processes the
tasks in a list of tasks. All the tasks require the same processing, so there's only one
task type, and one loop in the script.

    import logging
    import d1_common.utils.progress_logger

    def main():
        logging.basicConfig(level=logging.DEBUG)

        progress_logger = d1_common.utils.progress_logger.ProgressLogger()

        long_task_list = get_long_task_list()

        self.progress_logger.start_task_type(
            "My time consuming task", len(long_task_list)
        )

        for task in long_task_list:
            self.progress_logger.start_task("My time consuming task")
            do_time_consuming_work_on_task(task)
            if task.has_some_issue():
                progress_logger.event('Task has issue')

            if task.has_other_issue():
                progress_logger.event('Task has other issue')

        self.progress_logger.end_task_type("My time consuming task")

        self.progress_logger.completed()

Yields progress output such as:

    My time consuming task: 64/1027 (6.23% 0d00h00m)
    My time consuming task: 123/1027 (11.98% 0d00h00m)
    My time consuming task: 180/1027 (17.53% 0d00h00m)
    Events:
      Task has issue: 1
    My time consuming task: 236/1027 (22.98% 0d00h00m)
    Events:
      Task has issue: 2
      Task has other issue: 1
    My time consuming task: 436/1027 (32.98% 0d00h00m)
    Events:
      Task has issue: 2
      Task has other issue: 1
    My time consuming task: 636/1027 (44.12% 0d00h00m)
    Events:
      Task has issue: 2
      Task has other issue: 1
    Completed. runtime_sec=5.44 total_run_dhm="0d00h00m"

"""

import logging
import time

import d1_common.util


class ProgressLogger:
    def __init__(self, logger=None, log_level=logging.INFO, log_interval_sec=1.0):
        """Create one object of this class at the start of the script and keep a
        reference to it while the script is running.

        Args:
            logger:
                Optional logger to which the progress log entries are written. A new
                logger is created if not provided.

            level:
                The level of severity to set for the progress log entries.

            event_counter:
                Optional EventCounter to use for recording events

            log_interval_sec:
                Minimal time between writing log entries. Log entries may be written
                with less time between entries if the total processing time for a task
                type is less than the interval, or if processing multiple task types
                concurrently.

        """
        self._task_dict = {}
        self._event_dict = {}
        self._start_ts = time.time()
        self._last_log_time = time.time()
        self._log_interval_sec = log_interval_sec
        self._log = logger or logging.getLogger(__name__)
        self._log.setLevel(log_level)
        self._log_level = log_level

    def __del__(self):
        self._log_total_runtime()
        self._warn_if_active_task_types()

    def start_task_type(self, task_type_str, total_task_count):
        """Call when about to start processing a new type of task, typically just before
        entering a loop that processes many task of the given type.

        Args:
            task_type_str (str):
                The name of the task, used as a dict key and printed in the progress
                updates.

            total_task_count (int):
                The total number of the new type of task that will be processed.

        This starts the timer that is used for providing an ETA for completing all tasks
        of the given type.

        The task type is included in progress updates until end_task_type() is called.

        """
        assert (
            task_type_str not in self._task_dict
        ), "Task type has already been started"
        self._task_dict[task_type_str] = {
            "start_time": time.time(),
            "total_task_count": total_task_count,
            "task_idx": 0,
        }
        # self._log_msg('Started task type: {}'.format(task_type_str))
        # self._log_active_task_types()

    def end_task_type(self, task_type_str):
        """Call when processing of all tasks of the given type is completed, typically
        just after exiting a loop that processes many tasks of the given type.

        Progress messages logged at intervals will typically not include the final entry
        which shows that processing is 100% complete, so a final progress message is
        logged here.

        """
        assert (
            task_type_str in self._task_dict
        ), "Task type has not been started yet: {}".format(task_type_str)
        self._log_progress()
        del self._task_dict[task_type_str]
        # self._log_msg('Ended task type: {}'.format(task_type_str))

    def start_task(self, task_type_str, current_task_index=None):
        """Call when processing is about to start on a single task of the given task
        type, typically at the top inside of the loop that processes the tasks.

        Args:
            task_type_str (str):
                The name of the task, used as a dict key and printed in the progress
                updates.

            current_task_index (int):
                If the task processing loop may skip or repeat tasks, the index of the
                current task must be provided here. This parameter can normally be left
                unset.

        """
        assert (
            task_type_str in self._task_dict
        ), "Task type has not been started yet: {}".format(task_type_str)
        if current_task_index is not None:
            self._task_dict[task_type_str]["task_idx"] = current_task_index
        else:
            self._task_dict[task_type_str]["task_idx"] += 1
        self._log_progress_if_interval_elapsed()

    def event(self, event_name):
        """Register an event that occurred during processing of a task of the given
        type.

        Args:     event_name: str         A name for a type of events. Events of the
        same type are displayed as         a single entry and a total count of
        occurences.

        """
        self._event_dict.setdefault(event_name, 0)
        self._event_dict[event_name] += 1
        self._log_progress_if_interval_elapsed()

    def completed(self):
        """Call when about to exit the script.

        Logs total runtime for the script and issues a warning if there are still active
        task types. Active task types should be closed with end_task_type() when
        processing is completed for tasks of the given type in order for accurate
        progress messages to be displayed.

        """
        del self

    def _log_progress_if_interval_elapsed(self):
        if time.time() >= self._last_log_time + self._log_interval_sec:
            self._log_progress()
            self._last_log_time = time.time()

    def _log_progress(self):
        for task_type_str in sorted(self._task_dict):
            self._log_progress_for_task_type(task_type_str)
        self._log_events()

    def _log_events(self):
        if self._event_dict:
            self._log_msg("Events:")
            for event_str, count_int in sorted(self._event_dict.items()):
                self._log_msg("  {}: {}".format(event_str, count_int))

    def _log_progress_for_task_type(self, task_type_str):
        task_idx = self._task_dict[task_type_str]["task_idx"]
        total_task_count = self._task_dict[task_type_str]["total_task_count"]
        elapsed_sec = time.time() - self._task_dict[task_type_str]["start_time"]
        eta_sec = float(total_task_count) / (task_idx + 1) * elapsed_sec
        eta_str = d1_common.util.format_sec_to_dhm(eta_sec)
        self._log_msg(
            "{}: {}/{} ({:.2f}% {})".format(
                task_type_str,
                task_idx,
                total_task_count,
                task_idx / float(total_task_count) * 100,
                eta_str,
            )
        )

    def _log_msg(self, msg_str):
        self._log.log(self._log_level, msg_str)

    def _warn_if_active_task_types(self):
        if self._task_dict:
            self._log_progress()
            self._log.warning(
                "ProgressLogger was deleted while there were still active task types. "
            )
            self._log_active_task_types()

    def _log_active_task_types(self):
        if self._task_dict:
            self._log_msg('Active task types: {}'.format(", ".join(self._task_dict)))
        else:
            self._log_msg("Active task types: None")

    def _log_total_runtime(self):
        runtime_sec = time.time() - self._start_ts
        self._log_msg(
            'Completed. runtime_sec={:.02f} total_run_dhm="{}"'.format(
                runtime_sec, d1_common.util.format_sec_to_dhm(runtime_sec)
            )
        )
