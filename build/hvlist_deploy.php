<?php
require_once("deploy-token.php");

define("REMOTE_REPOSITORY", "https://github.com/kmzbrnoI/hJOPserverConfig");
define("DIR", "../serverRepos/dukelska-h0");
define("BRANCH", "refs/heads/mosilana-h0");
define("LOGFILE", "/dev/null");
define("GIT", "git");
define("MAX_EXECUTION_TIME", 15);
define("BEFORE_PULL", "git reset --hard @{u}");
define("AFTER_PULL", "cd .. && make all");

require("git-deploy/deployer.php");

define("REMOTE_REPOSITORY", "https://github.com/kmzbrnoI/hJOPserverConfig");
define("DIR", "../serverRepos/mendelu-tt");
define("BRANCH", "refs/heads/mendelu-tt");
define("LOGFILE", "/dev/null");
define("GIT", "git");
define("MAX_EXECUTION_TIME", 15);
define("BEFORE_PULL", "git reset --hard @{u}");
define("AFTER_PULL", "cd .. && make all");

require("git-deploy/deployer.php");
?>
