<?

	require_once("DatabaseTool.class.php");

	$from = $_GET["from"];

	switch($from)
	{
		default:
			echo "{}";
			break;

		case "users":
			require_once("UsersManager.class.php");
			$mgr = new UsersManager();
			echo json_encode($mgr->getall());
			break;

	}

?>