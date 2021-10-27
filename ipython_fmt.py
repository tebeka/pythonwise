def int_formatter(integer, pp, cycle):
    pp.text(f'{integer:,}')

plain = get_ipython().display_formatter.formatters['text/plain']
plain.for_type(int, int_formatter)
