$files = Get-ChildItem -Path . -Filter "*.md"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if (-not ($content -match "^---")) {
        $title = $file.BaseName -replace "_", " "
        $frontMatter = @"
---
layout: page
title: $title
permalink: /docs/$($file.BaseName)/
---

"@
        $newContent = $frontMatter + $content
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    }
} 