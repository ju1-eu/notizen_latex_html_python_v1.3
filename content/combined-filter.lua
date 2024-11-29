-- combined-filter.lua
function Cite(element)
    local citation = element.citations[1]
    if citation.mode == "NormalCitation" then
        return pandoc.RawInline('latex', '\\textcite{' .. citation.id .. '}')
    end
end
