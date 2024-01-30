import logging 

#################################################
#   log_config() needs to be initialized in     #
#   main() before any other function that uses  #
#   the log_error() function                    #
#################################################


def log_config():
    #--Create error.log file in same directory before running--#
    logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s - Line %(lineno)d')

def log_error(error :str):
    logging.error(f"An error occurred: {str(error)}", exc_info=True)



#--SAMPLE--#

"""
def main():
    log_config()

    try:
        x = "hello"
        y = x + 1
        print

    except Exception as e:
        log_error(e)

main()
"""
