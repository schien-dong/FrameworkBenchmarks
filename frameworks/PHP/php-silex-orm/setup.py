
import subprocess
import sys
import setup_util

def start(args, logfile, errfile):
  setup_util.replace_text("php-silex-orm/web/index.php", "192.168.100.102", "" + args.database_host + "")
  setup_util.replace_text("php-silex-orm/deploy/php-silex-orm", "\".*\/FrameworkBenchmarks/php-silex-orm", "\"" + args.troot)
  setup_util.replace_text("php-silex-orm/deploy/php-silex-orm", "Directory .*\/FrameworkBenchmarks/php-silex-orm", "Directory " + args.troot)
  setup_util.replace_text("php-silex-orm/deploy/nginx.conf", "root .*\/FrameworkBenchmarks/php-silex-orm", "root " + args.troot)

  try:
    #subprocess.check_call("sudo cp cake/deploy/cake /etc/apache2/sites-available/", shell=True)
    #subprocess.check_call("sudo a2ensite cake", shell=True)
    #subprocess.check_call("sudo chown -R www-data:www-data cake", shell=True)
    #subprocess.check_call("sudo /etc/init.d/apache2 start", shell=True)
    subprocess.check_call("composer.phar install", shell=True, cwd="php-silex-orm", stderr=errfile, stdout=logfile)
    subprocess.check_call("sudo $PHP_FPM --fpm-config $FWROOT/config/php-fpm.conf -g $TROOT/deploy/php-fpm.pid", shell=True, stderr=errfile, stdout=logfile)
    subprocess.check_call("sudo /usr/local/nginx/sbin/nginx -c $TROOT/deploy/nginx.conf", shell=True, stderr=errfile, stdout=logfile)
    return 0
  except subprocess.CalledProcessError:
    return 1
def stop(logfile, errfile):
  try:
    subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True, stderr=errfile, stdout=logfile)
    subprocess.call("sudo kill -QUIT $( cat $TROOT/deploy/php-fpm.pid )", shell=True, stderr=errfile, stdout=logfile)
    #subprocess.check_call("sudo a2dissite cake", shell=True)
    #subprocess.check_call("sudo /etc/init.d/apache2 stop", shell=True)
    #subprocess.check_call("sudo chown -R $USER:$USER cake", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1
