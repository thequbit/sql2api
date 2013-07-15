<?

	require_once("DatabaseTool.class.php");

	class UsersManager
	{
		function add($username,$passwordhash,$firstname,$lastname,$dob)
		{
			try
			{
				$db = new DatabaseTool(); 
				$query = 'INSERT INTO users(username,passwordhash,firstname,lastname,dob) VALUES(?,?,?,?,?)';
				$mysqli = $db->Connect();
				$stmt = $mysqli->prepare($query);
				$stmt->bind_param("sssss", $username,$passwordhash,$firstname,$lastname,$dob);
				$results = $db->Execute($stmt);
			
				$row = $results[0];
				$retVal = (object) array('userid' => $row['userid'],'username' => $row['username'],'passwordhash' => $row['passwordhash'],'firstname' => $row['firstname'],'lastname' => $row['lastname'],'dob' => $row['dob']);
	
				$db->Close($mysqli, $stmt);
			}
			catch (Exception $e)
			{
				error_log( "Caught exception: " . $e->getMessage() );
			}
		
			return $retVal;
		}

		function get($userid)
		{
			try
			{
				$db = new DatabaseTool(); 
				$query = 'SELECT * FROM users WHERE userid = ?';
				$mysqli = $db->Connect();
				$stmt = $mysqli->prepare($query);
				$stmt->bind_param("s", $userid);
				$results = $db->Execute($stmt);
			
				$row = $results[0];
				$retVal = (object) array('userid' => $row['userid'],'username' => $row['username'],'passwordhash' => $row['passwordhash'],'firstname' => $row['firstname'],'lastname' => $row['lastname'],'dob' => $row['dob']);
	
				$db->Close($mysqli, $stmt);
			}
			catch (Exception $e)
			{
				error_log( "Caught exception: " . $e->getMessage() );
			}
		
			return $retVal;
		}

		function getall()
		{
			try
			{
				$db = new DatabaseTool(); 
				$query = 'SELECT * FROM users';
				$mysqli = $db->Connect();
				$stmt = $mysqli->prepare($query);
				$results = $db->Execute($stmt);
			
				$retArray = array();
				foreach( $results as $row )
				{
					$object = (object) array('userid' => $row['userid'],'username' => $row['username'],'passwordhash' => $row['passwordhash'],'firstname' => $row['firstname'],'lastname' => $row['lastname'],'dob' => $row['dob']);
					$retArray[] = $object;
				}
	
				$db->Close($mysqli, $stmt);
			}
			catch (Exception $e)
			{
				error_log( "Caught exception: " . $e->getMessage() );
			}
		
			return $retArray;
		}

		function del($userid)
		{
			try
			{
				$db = new DatabaseTool(); 
				$query = 'DELETE FROM users WHERE userid = ?';
				$mysqli = $db->Connect();
				$stmt = $mysqli->prepare($query);
				$stmt->bind_param("s", $userid);
				$results = $db->Execute($stmt);
	
				$db->Close($mysqli, $stmt);
			}
			catch (Exception $e)
			{
				error_log( "Caught exception: " . $e->getMessage() );
			}
		}

		function update($username,$passwordhash,$firstname,$lastname,$dob)
		{
			try
			{
				$db = new DatabaseTool(); 
				$query = 'UPDATE users SET username = ?,passwordhash = ?,firstname = ?,lastname = ?,dob = ? WHERE userid = ?';
				$mysqli = $db->Connect();
				$stmt = $mysqli->prepare($query);
				$stmt->bind_param("ssssss", $username,$passwordhash,$firstname,$lastname,$dob, $userid);
				$results = $db->Execute($stmt);
	
				$db->Close($mysqli, $stmt);
			}
			catch (Exception $e)
			{
				error_log( "Caught exception: " . $e->getMessage() );
			}
		}

		///// Application Specific Functions

	}

?>
