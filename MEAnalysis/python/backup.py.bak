
        for k in ["DL_gen", "SL_2qW_gen", "SL_1qW_gen"]:
            self.configs[k].b_quark_candidates = lambda event: (
                event.b_quarks_gen if len(event.b_quarks_gen)>=4 else
                event.b_quarks_gen + event.unmatched_b_jets_gen
            )
            self.configs[k].l_quark_candidates = lambda event: event.l_quarks_gen
            self.configs[k].lepton_candidates = lambda event: event.good_leptons
            self.configs[k].met_candidates = lambda event: event.gen_MET
            self.configs[k].cfg.int_code |= MEM.IntegrandType.SmearJets
            self.configs[k].cfg.int_code |= MEM.IntegrandType.SmearMET
        for k in ["DL_gen_nosmear", "SL_2qW_gen_nosmear", "SL_1qW_gen_nosmear"]:
            self.configs[k].b_quark_candidates = lambda event: (
                event.b_quarks_gen if len(event.b_quarks_gen)>=4 else
                event.b_quarks_gen + event.unmatched_b_jets_gen
            )
            self.configs[k].l_quark_candidates = lambda event: event.l_quarks_gen
            self.configs[k].lepton_candidates = lambda event: event.good_leptons
            self.configs[k].met_candidates = lambda event: event.gen_MET
            #self.configs[k].cfg.int_code |= MEM.IntegrandType.Smear
        for x in ["SL_2qW", "SL_2qW_notag", "SL_2qW_gen", "SL_2qW_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 2
            )
        for x in ["SL_1qW", "SL_1qW_gen", "SL_1qW_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1
            )
            self.configs[x].mem_assumptions.add("1qW")
        for x in ["SL_0qW"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1
            )
            self.configs[x].mem_assumptions.add("0qW")
        for x in ["SL_1bT", "SL_1bTbar", "SL_1bH"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 3 and
                len(c.l_quark_candidates(y)) >= 2
            )
            k = x.split("_")[1]
            self.configs[x].mem_assumptions.add(k)
        for x in ["DL", "DL_gen", "DL_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 2 and
                len(c.b_quark_candidates(y)) >= 4
            )
            self.configs[x].mem_assumptions.add("dl")

        for k in [
                "SL_2qW", "SL_2qW_notag", "SL_1qW", "SL_2qW_gen",
                "SL_1qW_gen", "SL_2qW_gen_nosmear", "SL_1qW_gen_nosmear",
                "SL_0qW", "SL_1bT", "SL_1bTbar", "SL_1bH"
            ]:
            self.configs[k].mem_assumptions.add("sl")

        for x in ["SL_2w2h2t","SL_2w2h2t_btag",
                  "SL_2w2h1t_h", "SL_2w2h1t_l",
                  "SL_1w2h1t_h", "SL_1w2h1t_l"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 2 and
                y.cat_btag == "H"
            )
            self.configs[x].mem_assumptions.add("sl")

        self.configs["SL_2w2h2t_wtag"].l_quark_candidates = lambda event: event.wquark_candidate_jet_pairs[0] if len( event.wquark_candidate_jet_pairs )>0 else []
        for x in ["SL_2w2h2t_wtag"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 2 and
                y.cat_btag == "H"
            )
            self.configs[x].mem_assumptions.add("sl")

        for x in ["SL_1w2h2t", "SL_0w2h2t", "SL_0w2h2t_btag"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1 and
                y.cat_btag == "H"
            )
            self.configs[x].mem_assumptions.add("sl")

        for x in ["SL_0w2h2t_low_btag"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) == 3 and
                (len(c.l_quark_candidates(y))+len(c.b_quark_candidates(y))) >= 4 #and
                #y.cat_btag == "H"
                )
            self.configs[x].mem_assumptions.add("sl")

        for x in ["DL_low_btag"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 2 and
                len(c.b_quark_candidates(y)) >= 2 and
                (len(c.l_quark_candidates(y))+len(c.b_quark_candidates(y))) >= 4 #and
                #y.cat_btag == "H"
                )
            self.configs[x].mem_assumptions.add("dl")


        for x in ["SL_2w2h2t_btag", "SL_0w2h2t_btag", "SL_0w2h2t_low_btag", "DL_low_btag"]:
            strat = CvectorPermutations()
            strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
            #strat.push_back(MEM.Permutations.QUntagged)
            #strat.push_back(MEM.Permutations.BTagged)
            strat.push_back(MEM.Permutations.FirstRankedByBTAG)
            #strat.push_back(MEM.Permutations.FirstTwoRankedByBTAG)
            self.configs[x].cfg.perm_pruning = strat
            #    self.configs[x].cfg.b_range_CL = 0.9985
            #    self.configs[x].cfg.j_range_CL = 0.9985

        for k in ["SL_2w2h1t_h", "SL_2w2h1t_l",
                  "SL_1w2h1t_h", "SL_1w2h1t_l"]:
            self.configs[k].cfg.defaultCfg(1.5)

        for k in ["SL_2w2h2t","SL_2w2h2t_wtag", "SL_2w2h2t_btag",
                  "SL_1w2h2t", "SL_2w2h1t_h", "SL_2w2h1t_l",
                  "SL_0w2h2t", "SL_1w2h1t_h", "SL_1w2h1t_l", "SL_0w2h2t_btag", "SL_0w2h2t_low_btag"]:
            self.configs[k].cfg.do_prefit = 1

        self.configs["SL_2w2h2t"].mem_assumptions.add("2w2h2t")
        self.configs["SL_2w2h2t_btag"].mem_assumptions.add("2w2h2t")
        self.configs["SL_2w2h2t_wtag"].mem_assumptions.add("2w2h2t")
        self.configs["SL_1w2h2t"].mem_assumptions.add("1w2h2t")
        self.configs["SL_2w2h1t_l"].mem_assumptions.add("2w2h1t_l")
        self.configs["SL_0w2h2t"].mem_assumptions.add("0w2h2t")
        self.configs["SL_0w2h2t_btag"].mem_assumptions.add("0w2h2t")
        self.configs["SL_0w2h2t_low_btag"].mem_assumptions.add("0w2h2t")
        self.configs["SL_1w2h1t_h"].mem_assumptions.add("1w2h1t_h")
        self.configs["SL_1w2h1t_l"].mem_assumptions.add("1w2h1t_l")


        permutations = CvectorPermutations()
        #self.permutations.push_back(MEM.Permutations.BTagged)
        #self.permutations.push_back(MEM.Permutations.QUntagged)
        #self.permutations.push_back(MEM.Permutations.QQbarBBbarSymmetry)
        self.configs["SL_2qW_notag"].cfg.perm_pruning = permutations

        #Create additional configurations
        for strat, configure in [

                #Run with recoil instead of met
                ("Recoil", MEMConfig.configure_recoil),

                #apply sudakov factors
                ("Sudakov", MEMConfig.configure_sudakov),

                #apply sudakov factors
                ("NewTF", MEMConfig.configure_newtf),

                #run minimization
                ("Minimize", MEMConfig.configure_minimize)
            ]:
            for k in ["SL_2qW", "SL_1qW", "DL"]:
                kn = k + "_" + strat
                self.configs[kn] = copy.deepcopy(self.configs[k])
                self.configs[kn].cfg.defaultCfg()
                configure(self.configs[kn], self.configs[k])
