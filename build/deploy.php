<?php
require_once("deploy-token.php");

define("REMOTE_REPOSITORY", "https://github.com/kmzbrnoI/hvweb.git");
define("DIR", "..");
define("BRANCH", "refs/heads/master");
define("LOGFILE", "/dev/null");
define("GIT", "git");
define("MAX_EXECUTION_TIME", 180);
define("BEFORE_PULL", "git reset --hard @{u}");
define("AFTER_PULL", "(cd hvsrepo && git reset --hard origin/mosilana-h0 && git pull) && make all");

require_once("git-deploy/deployer.php");
