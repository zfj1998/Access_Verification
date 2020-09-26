import multiprocessing

workers = multiprocessing.cpu_count()
worker_class = "gevent" 
bind = "0.0.0.0:8008"
accesslog = './logs/acess.log'
errorlog = './logs/error.log'
pidfile = './logs/gunicorn.pid'
daemon = False
proc_name = "gunicorn_main"