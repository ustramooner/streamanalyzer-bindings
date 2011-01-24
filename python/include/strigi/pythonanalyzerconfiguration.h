#ifndef STRIGI_PYTHONANALYZERCONFIGURATION_H
#define STRIGI_PYTHONANALYZERCONFIGURATION_H

#ifdef SWIGGING
  %feature("director") PythonAnalyzerConfiguration;
  %rename (AnalyzerConfiguration) PythonAnalyzerConfiguration;
#endif
using namespace Strigi;


/**
 * @brief This class provides information and functions to control
 * the analysis.
 *
 * For example, it allows the files to be indexed to be limited based
 * on the name and path of the files.  It also stores the field
 * register (see AnalyzerConfiguration::fieldRegister and
 * Strigi::FieldRegister).
 *
 * It can be subclassed to provide finer control over the analysis
 * process.
 **/
class PythonAnalyzerConfiguration {
public:
    PythonAnalyzerConfiguration(){}
    virtual ~PythonAnalyzerConfiguration(){}
    
    /**
     * @brief Whether a given file should be indexed.
     *
     * In the default implementation, the path and filename
     * are checked against the filters specified by setFilters().
     * @p path is used if the filter pattern contains a /,
     * and @p filename is checked otherwise.
     *
     * The default implementation only checks against patterns
     * that do not end with @c /
     *
     * @param path the path to the file (eg: "/folder/a.txt")
     * @param filename the name of the file (eg: "a.txt")
     */
    virtual bool indexFile(const char* path, const char* filename) const { return true; }
    /**
     * @brief Whether a given directory should be indexed.
     *
     * In the default implementation, the path and filename
     * are checked against the filters specified by setFilters().
     * @p path is used if the filter pattern contains a /,
     * and @p filename is checked otherwise.
     *
     * The default implementation only checks against patterns
     * ending with @c /
     *
     * @param path the path to the directory, including
     * the directory name
     * @param filename the name of the directory
     */
    virtual bool indexDir(const char* path, const char* filename) const { return true; }

    /**
     * @brief Whether to use the given factory.
     *
     * Allows you to prevent the analyzers produced by a particular
     * factory from being used.
     *
     * The default implementation allows all factories.
     */
    virtual bool useFactory(StreamAnalyzerFactory*) const {
        return true;
    }
    
    /**
     * @brief Allows end analyzer to check whether they should continue
     * indexing.
     *
     * This should be called by end analyzers at convenient points to check
     * whether they should continue indexing.  For example, an end analyzer
     * analyzing a tar archive might call this to check whether it should
     * index the archive's children.
     *
     * This can be used to stop the indexing process at the next convenient
     * time.  For example, if the user wishes to interrupt the indexing
     * process, or if the tool @c deepgrep was asked to find the first
     * occurrence of a term and then stop.
     *
     * @return true if indexing should continue, false if it should stop
     */
    virtual bool indexMore() const {return true;}

    /**
     * @brief Allows end analyzer to check whether they should continue
     * adding text fragments to the index.
     *
     * This should be called by end analyzers before adding text
     * fragments with AnalysisResult::addText().
     *
     * This can be used to prevent the text index from being created,
     * or to prevent it from expanding.
     *
     * @return true if more text should be added to the index, false
     * if no more text should be added
     */
    virtual bool addMoreText() const {
        return true;
    }
    /**
     * @brief Return the maximal number of bytes that may be read from the
     * stream whose results are being written into @p ar.
     *
     * This function allows one to do analyses that only look at the first
     * bytes of streams for performance reasons. A scenario could be for getting
     * metadata for showing in a file manager.
     *
     * The individual analyzers should honour the value that is returned from
     * this function. They should also not assume that this value is constant
     * during the analysis and should regularly check whether they have not
     * read too much.
     *
     * @return the maximal number of bytes that may be read, or -1 if there is
     *         no limit
     **/
    virtual int64_t maximalStreamReadLength(const Strigi::AnalysisResult&/*ar*/) {
        return -1;
    }
};

}
#endif
