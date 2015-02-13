
class TTHSampleInput : public GenericInput
{

    std::vector<Sample> samples;
    //std::map<std::string> samples;
    const int nJobsTotal;
    const int nJobCurrent;
    long long perJob = 0;
    long long total = 0;

public:
    TTHSampleInput(const edm::ParameterSet &pset) :
        GenericInput(pset),
        nJobsTotal(pset.getParameter<int>("nJobsTotal")),
        nJobCurrent(pset.getParameter<int>("nJobCurrent"))
    {

        LOG(DEBUG) << "TTHSampleInput: created TTHSampleInput";

        for (auto &sample_pset : pset.getParameter<edm::VParameterSet>("samples"))
        {
            Sample s = Sample(sample_pset);
            s.treeS2->set_branch_addresses(125.0);
            s.treeS1->set_branch_addresses();
            samples.push_back(s);
        }

        total = getTotal();
        perJob = total / nJobsTotal;
        if (nJobCurrent <= 0 || nJobCurrent > nJobsTotal)
        {
            throw std::runtime_error("Current job index outside range");
        }

    };

    virtual long long getFirst()
    {
        return (nJobCurrent - 1) * perJob;
    }

    long long getTotal()
    {
        long long n = 0;
        for (auto &s : samples)
        {
            n += s.totalEvents;
        }
        return n;
    }

    virtual long long getLast()
    {
        if (nJobCurrent == nJobsTotal)
        {
            return total;
        }
        return nJobCurrent * perJob;
    }

    std::pair<int, long long> getSampleIndex(long long idx)
    {
        long long n = 0;
        int si = 0;
        long long first = 0;
        for (auto &s : samples)
        {
            first = n;
            n += s.totalEvents;
            if (idx < n)
            {
                return std::make_pair(si, first);
            }
            si += 1;
        }
        if (idx > n)
        {
            throw std::runtime_error("requested index  larger than total");
        }
        return std::make_pair(si, first);
    }

    virtual EventContainer getEvent(long long idx)
    {
        std::pair<int, long long> si = getSampleIndex(idx);
        std::pair<int, long long> si_prev = getSampleIndex(idx - 1);
        Sample &samp = samples[si.first];

        if (si_prev.first < si.first || idx == getFirst())
        {
            LOG(INFO) << "Sample changed " << currentName << "->" << samp.nickName;
            remakeSequences = true;
            currentName = samp.nickName;
        }
        else
        {
            remakeSequences = false;
        }

        long long loc_idx = idx - si.second;
        samp.treeS2->tree->GetEntry(loc_idx);

        LOG(DEBUG) << "sample index " << si.first << " local index " << loc_idx;
        EventContainer ev = EventContainer(idx);
        ev.addData<void *>("metree", samp.treeS2);
        ev.addData<void *>("sample", static_cast<void *>(&samp));

        processed++;
        return ev;
    }
};

template <class T>
GenericInput *createInputInstance(const edm::ParameterSet &pset)
{
    return new T(pset);
}