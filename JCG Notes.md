Major questions:

* What's the difference between big_search.py, seti_offline_analysis.py, and seti_algorithm_working_version.py?
* Are decision_tree.py, rawframe_analyzer.py, raw_data_downloader.py being used?
    -- decision_tree.py = no
    -- rawframe_analyzer.py = no
    -- raw_data_downloader.py = no

* Which of these files can be consolidated?

Files and their purposes:

* big_search.py
    -- Search through a list of stars, run seti_spike_analyzer on each.
    -- Called by test/run_test.py
    
* decision_tree.py
    -- Search through a list of stars and categorize them by total number of spikes.
    -- Not called by anything

* downloader.py
    -- Download one spectrum from each of the targets listed in OSETI_survey1.txt, store in cache.
    -- Should be integrated in with big_search.py

* gaussian_curve_fitting_algorithm.py
    -- Fit a Gaussian curve to a spectral line found at hits_start to hits_end, plot both, print the width of the Gaussian fit.
    -- Needs cleanup and generalization
    -- Not called by any other .py

* harpscompare.py
    -- Code to download HARPS spectral and CCD data, and plot it side-by-side.  
    -- Not called by any other .py

* harps_spectralpositioning.txt
    -- XY location of spectral orders on CCD image 
    -- Used by harpscompare.py

* JCG Notes.txt
    -- This file

* optical_seti_functions.py
    -- Main module for this project
    -- Used by:
        + big_search.py
        + decision_tree.py
        + downloader.py
        + gaussian_curve_fitting_algorithm.py
        + seti_algorithm_working_version.py
        + seti_offline_analysis.py

* OSETI_targets.txt
    -- Main list of stars to analyze

* rawframe_analyzer.py
    -- Early version of harpscompare?
    -- Not used, deleted.

* raw_data_downloader.py
    -- Download HARPS CCD data for files in "category2.txt"
    -- Not used, deleted

* raw_download_record.txt
    -- Files downloaded by raw_data_downloader.py

* README.md
    -- Needs a *LOT* of work

* seti_algorithm_working_version.py
    -- Search through a list of stars, run seti_spike_analyzer on each.
    -- Similar to big_search.py and seti_offline_analysis.py

* seti_offline_analysis.py
  -- Search through a list of stars, run seti_spike_analyzer on each.
  -- Similar to big_search.py and seti_offline_analysis.py

