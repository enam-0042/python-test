import logging

app_logger = logging.getLogger('_handlers_demo_')
app_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
app_logger.addHandler(console_handler)




console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)


app_logger.info("This log message is going to both the console and the file.")
app_logger.warning("This is a warning that will also appear in both places.")
app_logger.debug("This message will NOT be logged because the level is set to INFO.")





file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

app_logger.addHandler(file_handler)

app_logger.info("This log message is going to both the console and the file.")
app_logger.warning("This is a warning that will also appear in both places.")
app_logger.debug("This message will NOT be logged because the level is set to INFO.")
