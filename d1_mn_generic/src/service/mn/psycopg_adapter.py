import psycopg2.extensions
import pyxb.binding.datatypes
import d1_common.types.generated.dataoneTypes

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


def adapt_pyxb_binding(binding):
  return psycopg2.extensions.AsIs(u"'{0}'"\
    .format(unicode(binding)))
  # An example uses adapt() here, but I could not get that to work with
  # casting to unicode. It works with casting to str.
  #.format(psycopg2.extensions.adapt(str(binding))))


psycopg2.extensions.register_adapter(
  d1_common.types.generated.dataoneTypes.ObjectFormatIdentifier, adapt_pyxb_binding
)

psycopg2.extensions.register_adapter(pyxb.binding.datatypes.string, adapt_pyxb_binding)

psycopg2.extensions.register_adapter(pyxb.binding.datatypes.boolean, adapt_pyxb_binding)
