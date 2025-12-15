import logging
logger = logging.getLogger("formatter_demo")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
# Attach the simple formatter to our handler.
handler.setFormatter(simple_formatter)



logger.info("This is an informational message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")



detailed_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
# Attach the detailed formatter to the same handler.
handler.setFormatter(detailed_formatter)

# Log the same messages again to see the difference in output.
# The output will now include extra information.
logger.info("This is an informational message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")