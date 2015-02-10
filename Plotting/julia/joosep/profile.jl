using ProfileView
include("ntuple.jl")
Analysis.main()
Profile.init(n=1000000000)
@profile Analysis.main()
ProfileView.svgwrite("profile.svg")
