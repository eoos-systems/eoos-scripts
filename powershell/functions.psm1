<##
 # This script contains some useful functions.
 #
 # @author Sergey Baigudin, sergey@baigudin.software
 #>
 
<## 
 # Outs a message.
 #>
function Out-Message([string]$string, [switch]$block, [switch]$say, [switch]$ok, [switch]$err, [switch]$inf)
{
    [string]$line = "-------------------------------------------------------------------------------"
   
    [ConsoleColor]$color = "Gray"
    if($ok)
    {
        $color = "Green"
    }    
    if($err)
    {
        $color = "Red"
    }
    if($inf)
    {
        $color = "Yellow"
    }   
        
    if($block)    
    {
        Write-Host $line -ForegroundColor $color
        $string = " " + $string
    }    

    Write-Host $string -ForegroundColor $color
    
    if($block)    
    {
        Write-Host $line -ForegroundColor $color
    }
    
    if($say)
    {
        Out-Speech $string
    }    
} 

<## 
 # Out a speech.
 #>
function Out-Speech([string]$string, [switch]$demanded)
{
    $voice = New-Object -com "SAPI.spvoice"
    $voice.rate = -1
    $voice.volume = 100
    $voice.voice = $voice.getVoices().item(0)    
    $voice.speak($string) > $null
}


Export-ModuleMember -function Out-Message
Export-ModuleMember -function Out-Speech