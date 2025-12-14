from  apscheduler.schedulers.asyncio import AsyncIOScheduler
from data.save_file import check_and_save_file
from core.config import settings
from core.log_config import get_logger
from datetime import datetime
logger = get_logger()
scheduler = AsyncIOScheduler()
logger.debug(scheduler)



def check_and_update_job():
    logger.info('APScheduler Triggered')
    try:
        check_and_save_file(forced_call=False)
    except Exception as e:
        logger.error(f'Error in scheduled job: {e}')

def start_scheduler():
    scheduler.add_job(
        check_and_update_job,
        trigger="interval",
        seconds=settings.OVERLOOK_MINUTES,
        # next_run_time=datetime.utcnow(),
        id="check_and_update_job",
        replace_existing=True,        
        max_instances=1,
        coalesce=True,
       
    )
    scheduler.start()
    logger.info("scheduler started")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("scheduler stopped")
