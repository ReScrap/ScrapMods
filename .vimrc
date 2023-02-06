" %E%.%# %f:%l
" %CLine |
" %C %#%*[0123456789] %#| %.%#
" %-C %#| %#~%#
" %C %#| %m
" %Z
"
" %ETraceback %.%#:
" %C  File "%f", line %l,%.%#
" %C    %.%#
" %Z%m

" set makeprg=pwsh\ -c\ .\\Police2Gear\\build.ps1
set makeprg=pwsh\ -c\ .\\build.ps1
set efm=%-G,
      \%trror:\ %m,
      \%E%.%#\ %f:%l,
      \%CLine\ \|,
      \%C\ %#%*[0123456789]\ %#\|\ %.%#,
      \%-C\ %#\|\ %#~%#,
      \%C\ %#\|\ %m,
      \%Z,
      \%ETraceback\ %.%#:,
      \%C\ \ File\ \"%f\"\\,\ line\ %l\\,\ %.%#,
      \%C\ \ \ \ %.%#,
      \%Z%m

