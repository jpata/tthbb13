using DataFrames, ROOT, ROOTDataFrames

length(ARGS)==1 || error("ntuple.jl file.root")

fn = ARGS[1]
isfile(fn) || error("File error: $fn")

df = TreeDataFrame(ASCIIString[fn], "tthNtupleAnalyzer/events")

function parse_event(df::TreeDataFrame, i::Int64)
end

for i=1:nrow(df)
end
