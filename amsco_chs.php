<?php


$metadata_dir = "Metadata\\StatDescriptions\\";
$ldir = "Metadata_utf8\\";
$ddir = "Metadata_chs\\";
	if (!file_exists($ldir)) {
		echo "$ldir\\\n";
		mkdir($ldir);
	}
	if (!file_exists($ddir)) {
		echo "$ddir\\\n";
		mkdir($ddir);
	}
if (is_dir($metadata_dir)) {
    if ($dh = opendir($metadata_dir)) {
        while (($file = readdir($dh)) !== false) {
            if ($file == "." || $file == "..") continue;
            echo "filename: $file : filetype: " . filetype($metadata_dir . $file) . "\n";
            to_utf8($metadata_dir, $ldir, $file);
			tcc($ldir, $ddir, $file);
			unlink($ldir.$file);
        }
        closedir($dh);
    }
	rmdir($ldir);
}

// Open a known directory, and proceed to read its contents
function to_utf8($metadata_dir, $ldir, $file)
{
	$contents = file_get_contents($metadata_dir . $file);
	$contents = iconv("UCS-2LE", "UTF-8", $contents);
	$lcontents = file_get_contents($ldir.$file);
	
	$outs = "";
	$lines = explode("\r\n", $contents);
	foreach($lines as $line) {
		if (substr($line, 0, strlen("description")) == "description") {
			$indes = 1;
			$outs .= "\r\n";
		}
		if ($indes && trim($line) == "") {
			continue;
		}
		$outs .= $line."\r\n";
	}
	$contents = str_replace("\r\n\r\n\r\n", "\r\n\r\n", $outs);
	//echo $outs; exit();
	//print_r($lines); exit();
	
	if ($contents != $lcontents) {
		echo $file." replaced\n";
		file_put_contents($ldir.$file, $contents);
	} else {
		echo $file."\n";
	}
}

function tcc($d, $d_tc, $f)
{
    $lines = file($d.$f);
    for($i=0; $i<sizeof($lines); $i++) {
        $line = $lines[$i];
        $t = ($line);
//echo $t."\n";
        if (substr(trim($t), 0, strlen("description")) == "description") {
            $outs .= ltrim($line);
            $i++; $line = $lines[$i]; // 1 num_of OR blank line
            if (trim($line) == "") {
                $i++; $line = $lines[$i];
            }
            $outs .= $line;
            $i++; $line = $lines[$i];
            //$outs .= $line;
            $skip = intval(trim($line));
            if (is_numeric($skip)) {
                $engs = $line;
                for($j=0; $j<$skip; $j++) {
                    $i++; $line = $lines[$i];
                    if (trim($line) == "") {
                        $i++; $line = $lines[$i];
                    }
                    $engs .= $line;
                }
                $i++; $line = $lines[$i]; // lang "Simplified Chinese"
                if (trim($line) == "") {
                    $i++; $line = $lines[$i];
                    $skip_blank = true;
                } else {
                    $skip_blank = false;
                }
				$tc = false;
				while(1) {
					if (!$tc && trim($line) == 'lang "Simplified Chinese"') {
						$i++; $line = $lines[$i];
						$tc_skip = intval(trim($line));
						//$i += $tc_skip;
						$outs .= $line; // tc_skip
						for($j=0; $j<$tc_skip; $j++) {
							$i++; $line = $lines[$i];
							if (trim($line) == "") {
								$i++; $line = $lines[$i];
							}
							$outs .= $line;
						}
						$tc = true;
						$i++; $line = $lines[$i];
						//$outs .= "\r\n";
					} else if (substr(trim($line), 0, 5) == "lang ") {
					$i++; $line = $lines[$i];
						$tc_skip = intval(trim($line));
						//$i += $tc_skip;
						//$outs .= $line; // tc_skip
						for($j=0; $j<$tc_skip; $j++) {
							$i++; $line = $lines[$i];
							if (trim($line) == "") {
								$i++; $line = $lines[$i];
							}
							//$outs .= $line;
						}
						$i++; $line = $lines[$i];
					} else {
						break;
					}
				}
				if (!$tc) {
						$outs .= $engs;
						if ($skip_blank)
							$i--;
				}
				$i--;

                //$i += ($skip+1);
            } else {
                echo "err $skip\n";
                exit();
            }
			//echo $outs; exit();
            continue;
        }
        $outs .= $line;
    }
	$outs = iconv("UTF-8", "UCS-2LE", $outs);
    file_put_contents($d_tc.$f, $outs);
}

?>