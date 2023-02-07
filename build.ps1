param(
  [Parameter()]
  [String] $mod_folder,
  [Switch] $verbos,
  [Switch] $install,
  [Switch] $uninstall
)

$packed_explorer_path = '.\bins\spe.exe';
$pyhton_path          = 'C:\Program Files (x86)\Python\python.exe';
$scrapland_path       = 'D:\Games\SteamLibrary\steamapps\common\Scrapland';

if (-not (Test-Path(".\config.ps1"))) {
  Copy-Item .\config.example.ps1 .\config.ps1;
}

. "$PSScriptRoot\config.ps1"

$output_path    = ".\out"

$pack_expl_name = 'ScrapPackedExplorerCli';
$pack_expl_ver  = [version]'0.3.1';

$userless_err_msgs = @(
  "ImportError: No module named Scrap",
  "ImportError: No module named SAI",
  "ImportError: No module named SAct",
  "ImportError: No module named SFX",
  "ImportError: No module named SInput",
  "ImportError: No module named SLogic",
  "ImportError: No module named SNet",
  "ImportError: No module named SScorer",
  "ImportError: No module named SSound",
  "ImportError: No module named SVec",
  "ImportError: No module named SWeap"
);

$folders_exclude = (
  'bins',
  'out'
);

function quite_rm($path) {
  Remove-Item $path 2>&1 | out-null;
}

function is_string_in_array($string, $array) {
  return $null -ne ($string | Where-Object { $array -match $_ });
}

function disable_colorded_output() {
  $PSStyle.OutputRendering = [System.Management.Automation.OutputRendering]::PlainText;
}

function normalize_mod_name($mod) {
  $mod = $mod.TrimEnd("\");
  $mod = $mod.TrimStart(".\");
  return $mod;
}

function check_pack_expl() {
  if (-not (test-path $packed_explorer_path)) {
    Write-Output "Error: $pack_expl_name was not found at '$packed_explorer_path'. Please download $pack_expl_name >= $pack_expl_ver";
    exit 1;
  }

  # --version outputs to stderr;
  $err = (& $packed_explorer_path --version) 2>&1;
  $spe_version = $err[0].ToString();

  $null = $spe_version -match '(?<name>[^\d]+)(?<version>\d.+)';
  $name, $version = $Matches['name'].TrimEnd('.').Trim(), [version]$Matches['version'];

  $is_pack_expl_good = $name -ne $pack_expl_name -or
                       $version.Major -lt $pack_expl_ver.Major -or
                       $version.Minor -lt $pack_expl_ver.Minor -or
                       $version.Build -lt $pack_expl_ver.Build;

  if ($is_pack_expl_good) {
    Write-Output "Error: wrong binary at '$packed_explorer_path'. $name >= $version needed.";
    exit 1;
  }
}

function compile_pyhton($mod) {
  Push-Location $mod

  Get-ChildItem "." -Recurse -Filter *.py | Foreach-Object {
    Push-Location $_.Directory.FullName

    $file_name = $_.Name

    # NOTE: Pyhton will not compile with `pyhton $file_name` because of import errors
    #       but if we try to import required file it will compile
    $output = (& $pyhton_path -c "import $file_name")  2>&1

    # Surpressing error messages about Scrap/SInput/etc module not found
    if (-not (is_string_in_array $output $userless_err_msgs) -or $v -or $verbos) {
      # Additional empty lines for better errorformat parsing in vim. Check .vimrc for more info
      Write-Output "$mod/../$file_name";
      Write-Output ""
      Write-Output $output
      Write-Output ""
    }

    Pop-Location
  }

  Pop-Location
}

function pack_mod($mod) {
  quite_rm "$output_path\$mod.packed";

  if (Test-Path $mod\packed\) {
    & $packed_explorer_path "$output_path\$mod.packed" add -s $mod\packed;
    return;
  } else {
    & $packed_explorer_path "$output_path\$mod.packed" add -s $mod\;
    & $packed_explorer_path "$output_path\$mod.packed" remove -d README.md;
  }
}

function load_mod($mod) {
  unload_mod($mod);
  Copy-Item "$output_path\$mod.packed" $scrapland_path\Mods;
}

function unload_mod($mod) {
  if (test-path "$scrapland_path\Mods\$mod.packed") {
    quite_rm "$scrapland_path\Mods\$mod.packed";
  }
}

function load_mod_languages($mod) {
  if (-not (Test-Path $mod\lang\)) {
    return;
  }

  $mod_lang_folder = "$scrapland_path\Language\$mod";

  if (-not (Test-Path $mod_lang_folder)) {
    mkdir $mod_lang_folder | Out-Null;
  }

  Copy-Item $mod\lang\* $mod_lang_folder;
}

function unload_mod_languages($mod) {
  if (-not (Test-Path $mod\lang\)) {
    return;
  }

  Remove-Item -Recurse "$scrapland_path\Language\$mod\";
}

function build_game_languages() {
  $lang_path = "$scrapland_path\Language";

  Get-ChildItem $lang_path -File -Filter *.txt.bak | ForEach-Object {
    Copy-Item $_ ($_.FullName.Replace(".bak", "")) -Force
  }

  Get-ChildItem $lang_path -Directory | ForEach-Object {
    Get-ChildItem $_ -Filter *.txt | ForEach-Object {
      if (-not (Test-Path "$lang_path\$($_.Name).bak")) {
        Copy-Item "$lang_path\$($_.Name)" "$lang_path\$($_.Name).bak" -Force;
        Write-Output "" >> $lang_path\$($_.Name);
      }

      Get-Content $_ >> $lang_path\$($_.Name);
    }
  }
}

function build_mod($mod) {
  compile_pyhton($mod);
  pack_mod($mod);
}

function install_mod($mod) {
  load_mod($mod);
  load_mod_languages($mod);
}

function uninstall_mod($mod) {
  unload_mod($mod);
  unload_mod_languages($mod);
}

function make_all_mods() {
  Get-ChildItem "." -Dir | Foreach-Object {
    if (-not (is_string_in_array $_.Name $folders_exclude)) {
      make_mod($_.Name);
    }
  }
}

function uninstall_all_mods() {
  Get-ChildItem "." -Dir | Foreach-Object {
    if (-not (is_string_in_array $_.Name $folders_exclude)) {
      uninstall_mod($_.Name);
    }
  }
}

function make_mod($mod) {
  build_mod($mod);

  if ($install) {
    install_mod($mod);
  }
}

function main() {
  disable_colorded_output;
  check_pack_expl;
  $mod_folder = normalize_mod_name($mod_folder);

  if (-not $mod_folder) {
    if ($uninstall) { uninstall_all_mods; } else { make_all_mods; }
    build_game_languages;
    return;
  }


  if (is_string_in_array $mod_folder $folders_exclude) {
    return;
  }

  if ($uninstall) { uninstall_mod($mod_folder); } else { make_mod($mod_folder); }
  build_game_languages;
}

main
