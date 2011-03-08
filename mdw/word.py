# tutorials are here: http://win32com.goermezer.de/content/category/7/86/192/
# object reference http://msdn.microsoft.com/en-us/library/aa272131(v=office.11).aspx
import win32com.client as win32
import re, sys
import traceback
from win32com.client import constants

msoPropertyTypeBoolean = 0
msoPropertyTypeDate = 1
msoPropertyTypeFloat = 2
msoPropertyTypeNumber = 3
msoPropertyTypeString = 4

class Document():
    def __init__(self, filepath):
        self.__filpath = filepath
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.word.Visible = False
        self.doc = self.word.Documents.Open(filepath)
    def setCustomProperty(self, name, value):
        self.__setProperty(self.doc.CustomDocumentProperties, name, value)

    def setBuiltInDocumentProperty(self, name, value):
        self.__setProperty(self.doc.BuiltInDocumentProperties, name, value)
        
    
    def __setProperty(self, properties, name, value):
        try:
            properties[name] = value
        except:
            properties.Add(name, False, msoPropertyTypeString, value)
    def saveAs(self, filepath):
        self.doc.Saved = False
        self.doc.SaveAs(filepath)
    def close(self):
        self.doc.Close(False)
        self.word.Application.Quit()
    def replace_text(self, selection, text, replace_text):
        """
        replace using wildcards in text variable

        """
        find = selection.Find
        find.ClearFormatting()
        find.Text = text
        find.Replacement.Text = replace_text
        find.MatchWildcards = True
        find.MatchWholeWord = False
        find.MatchCase = False
        #find.IgnoreSpace = True
        #replace all
        find.Execute(Replace=2)

    def findAndSelect(self, selection, text):
        selection.SetRange(selection.End, self.doc.Range.End) 
        find.ClearFormatting()
        find.Text = text
        find.MatchWildcards = True
        find.MatchWholeWord = False
        find.MatchCase = False
        find.IgnoreSpace = True
        find.Forward = True
        find.Execute()
        if find.Found:
            sel = find.Selection
            return sel
        else:
            return None

    def extend_to_sentence(self, selection):
        """
        The passed in selection should be some selected word.
        This method extends the selection to the whole sentence containing the word.
        """
        selection.Collapse()
        selection.Extend()
        selection.Extend()
        selection.Extend()
        return selection

    def get_table(self, bookmark):
        bookmark = self.doc.Bookmarks(bookmark)
        tables = bookmark.Range.Tables
        if len(tables) < 1:
            print "Error: Could not find table with bookmark %s" % bookmark
        elif len(tables) > 1:
            print "Error: Found several tables with bookmark %s" % bookmark 
        else:
            return tables[0]
        
class SrsDocument(Document):
    def __init__(self, filepath):
        Document.__init__(self, filepath)
        
    def replace_baselines(self, newComponentVersionBaseline):
        """
        Searches for all sentences containing the word Baseline and replaces baselines
        with the new baseline.
        see replace_baseline for some restrictions.
        """
        countReplaced = 0
        
        for sentence in self.doc.Sentences:
            sentence.Select()
            replaced = self.replace_baseline(self.word.Selection, newComponentVersionBaseline)
            if replaced:
                countReplaced += 1
        print "Replaced %d baseline(s) with %s" % (countReplaced, newComponentVersionBaseline)
        
    def replace_baseline(self, selection, newComponentVersionBaseline):
        """
        Searches for baseline assignments (Baseline = "some baseline") in the given selection
        and replaces it with the new baseline.
        If there are several baseline assignments in the same sentence, then no replacement is done.
        Reason: Queries with several baselines are likely to be used in the history table as diff
        between to versions and they should not be replaced.
        """
        text = selection.Text
        p = re.compile(r'Baseline\s*=\s*"[^"]*"', re.IGNORECASE)        
        matches = p.findall(text)
        replaced = False
        if matches:
            if len(matches) > 1:
                print "Not replacing baseline, where it is several times in the same sentence: %s" % str(matches)
            elif len(matches) == 1:
                replace_text = 'Baseline = "%s"' % newComponentVersionBaseline
                print "Replacing <%s> by <%s>" % (matches[0], replace_text)
                self.replace_text(selection, matches[0], replace_text)
                replaced = True
        #else:
            #print "Did not replace baseline in %s" % text
        return replaced
      
    def add_history_entry(self, author, previous_baseline, new_baseline):
        table = self.get_table("history")
        row = table.Rows.Add()
        cells = row.Cells
        cells[0].Range.Text = author
        change_col_index = 1
        insert_range = cells[change_col_index].Range
        insert_range.Text = "Baseline = %s" % new_baseline
        insert_range.InsertParagraphAfter()
        table_range = insert_range.Paragraphs(1).Range
        table_range.InsertParagraphAfter()
        req_table = self.doc.Tables.Add(insert_range.Paragraphs(2).Range, 1, 3, constants.wdWord9TableBehavior, constants.wdAutoFitContent)
        req_table.Cell(1,1).Range.Text = "RequirementId"
        req_table.Cell(1,2).Range.Text = "Note"
        req_table.Cell(1,3).Range.Text = "Synopsis"

    def accept_all_changes():
        pass
     
def create_newsrs():
    try:
        filepath="E:\\data\\projects\\test\\a.doc"
        new_filepath="E:\\data\\projects\\test\\a2.doc"
        doc = SrsDocument(filepath)
        new_version = "1.2STD3"
        doc.setCustomProperty("Issue", new_version)
        new_baseline = "C_SMM_3_4STD5"
        doc.replace_baselines(new_baseline)
        doc.add_history_entry("E. Hofmann", "C_SMM_3_4STD4", new_baseline)
        #selections = doc.find_baselines()
        #for s in selections:
        #    print "Selection text: %s" % s.Text
        print "Before save"
        doc.saveAs(new_filepath)
    except Exception,e:
        print "Exception: %s" % e
        traceback.print_exc(file=sys.stdout)
    finally:
        doc.close()

def word():
    filepath="E:\\data\\projects\\test\\a.doc"
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(filepath)
    oBuiltInProps = doc.BuiltInDocumentProperties 
    author = oBuiltInProps["Author"]

    print "Author: %s" % author
    oCustomProps = doc.CustomDocumentProperties
    versionString = "2.3STD4"
    try:
        oCustomProps["version"] = versionString
    except:
        oCustomProps.Add("version", False, 4, versionString)
        
    doc.Saved = False
    doc.Save()
    doc.Close(False)
    word.Application.Quit()
 
if __name__ == '__main__':
    create_newsrs()

