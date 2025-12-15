import logging 
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(name)s - %(levelname)s - %(message)s')
)

parent_logger = logging.getLogger("parent_logger")
child_logger = logging.getLogger("parent_logger.child")

parent_logger.addHandler(console_handler)
parent_logger.setLevel(logging.INFO)
child_logger.setLevel(logging.INFO)

child_logger.info("This message is from the child and will propagate up.")
parent_logger.warning("This message is from the parent.")

child_logger.propagate = False
child_logger.info("This message will NOT be displayed because propagation is off.")
parent_logger.warning("This message from the parent still works as before.")



