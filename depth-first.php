<?php 
$a = [
	1=>[
		2=>[
			3=>[
				4=>[],
				5=>[]
			],
			6=>[]
		],
		7=>[
			9=>[]
		],
		8=>[
			12=>[],
			9=>[
				10=>[],
				11=>[]
			]
		]
	]
];
$a = [
	'v'=>1,
	'node'=>
	[
		'v'=>2,
		'node'=>
		[
			'v'=>3,
			'node'=>
			[
				'v'=>4,
				'v'=>5
			]
		],
		[
			'v'=>6
		]
	],
	[
		'v'=>7
	],
	[
		'v'=>8,
		'node'=>
		[
			'v'=>9,
			'node'=>
			[
				'v'=>10,
				'v'=>11
			]
			
		],
		[
			'v'=>12
		]
	]
];
/*
function depthFirst($array,$find) {
	print_r($array);
	echo "\n";
	if(empty($array))return false;
	foreach ($array as $key => $value) {
		echo $key." ".$value." ".$find."\n";
		if($key == $find) {
			//print "got here ".__LINE__."\n";
			return $value;
		}
		if(is_array($value)){
			$return = depthFirst($value,$find);
			if(false !== $return) {
				//print "got here ".__LINE__."\n";
				return $return;
			}
		}else{
			if($value == $find) {
				//print "got here ".__LINE__."\n";
				return $value;
			}else{
				return false;
			}
		}
	}
}
*/
$found = false;
function depthFirst($array,$find) {
	global $found;
	
	//print "\n".$array['v']."\n";
	print_r($array);
	echo "\n";
	if($array['v']==$find) {
		$found = true;
		return $array;
	}
	if(isset($array['node']))
		//return false;

	foreach ($array['node'] as $key => $value) {
		//if($key=='node') {
			$result = depthFirst($value,$find);
			//if(false === $result)
			//	return false;
			if($found === true) {
				return $result;	
			}
		//}
	}
	if(false === $found)
		return false;
}

$r = depthFirst($a,8);

if(true===$found)
	echo "\n\nFound it!";

echo "\n\nResult:\n";
print_r($r);
echo "\n\n";

