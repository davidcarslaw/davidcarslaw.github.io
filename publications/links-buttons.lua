-- Render `links:` YAML front matter as Bootstrap icon buttons
-- Applied via publications/_metadata.yml
function Pandoc(doc)
  local meta = doc.meta
  if not meta.links then
    return doc
  end

  local html = '<div class="publication-links mb-3">\n'
  for _, link in ipairs(meta.links) do
    local icon = link.icon and pandoc.utils.stringify(link.icon) or ''
    local name = link.name and pandoc.utils.stringify(link.name) or ''
    local url  = link.url  and pandoc.utils.stringify(link.url)  or '#'
    html = html .. string.format(
      '  <a href="%s" class="btn btn-outline-primary btn-sm me-2" target="_blank">' ..
      '<i class="bi bi-%s"></i> %s</a>\n',
      url, icon, name
    )
  end
  html = html .. '</div>\n'

  table.insert(doc.blocks, 1, pandoc.RawBlock('html', html))
  return doc
end
