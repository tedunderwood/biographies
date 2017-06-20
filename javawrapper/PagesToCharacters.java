package novels;
import java.util.UUID;
import java.io.IOException;

/**
 * @author tunder
 *
 */
public class PagesToCharacters {
	/**
	 * This is simply a wrapper for bookNLP, by David Bamman. Its only purpose
	 * is to iterate through a list of files. In each case it selects specified
	 * pages from that file, concatenates them, and writes the resulting text
	 * file to disk as a temporary object. Then it passes that path to BookNLP.main
	 * which does the real work.
	 * 
	 * @param args 	an array containing a single string, which is a path to
	 * 				0) a file containing filepaths to be processed, and
	 * 				1) a directory where processed files get output.
	 *
	 */
	
	public static void main(String[] args) {
		// This method receives a path to a file, which is expected to be a
		// tab-separated list with four columns:
		
			// 0) bookids
			// 1) paths to the associated zip file for each id.
			// 2) Page number where the text begins.
			// 3) Page number *after* the last page included in text.
			// standard deal where the start is inclusive and the end isn't
		
			// This is not maximally general; it does not permit skipping pages;
			// that's okay.
		
		// args should also provide a second argument, an output directory.
		
		// String holdingfolder = "/projects/ichass/usesofscale/sampletexts/";
		String holdingfolder = "/media/secure_volume/temp/";
		
		String pathToListOfSources = args[0];
		String outputDir = args[1];
		// Note that this does not require a trailing slash; it can be, e.g.,
		// "data/output/collected"
		
		// Create a random name for your temp file
		String uuid = UUID.randomUUID().toString();
		String tempfile = holdingfolder + uuid.substring(0, 8) + ".txt";
		LineWriter tempWriter = new LineWriter(tempfile, false); // False meaning do not append; overwrite.
		
		LineReader pathReader = new LineReader(pathToListOfSources);
		String[] allSources = pathReader.readlines();
		
		for (String aSource : allSources) {
			String[] quartet = aSource.split("\t", 4);
			String bookid = quartet[0];
			String sourcePath = quartet[1];
			int startPage = Integer.parseInt(quartet[2]);
			int endPage = Integer.parseInt(quartet[3]);
			
			System.out.println(bookid);
			
			try {
				String[] pageArray = ZipReader.getPages(sourcePath, startPage, endPage);
				pageArray = HeaderZapper.zapaway(pageArray);
				tempWriter.send(pageArray);
			}
			catch(IOException e) {
				e.printStackTrace();
				continue;	
			}
			
			String[] argsToPass = new String[9];
			argsToPass[0] = "-doc";
			argsToPass[1] = tempfile;
			argsToPass[2] = "-id";
			argsToPass[3] = bookid;
			argsToPass[4] = "-p";
			argsToPass[5] = outputDir;
			argsToPass[6] = "-tok";
			argsToPass[7] = "/media/secure_volume/tokens/" + bookid + ".tokens";
			// argsToPass[7] = "/projects/ichass/usesofscale/sampletexts/tokens/" + bookid + ".tokens";
			argsToPass[8] = "-f";
			
			try {
				BookNLP.main(argsToPass);
			}
			catch (Exception e){
				e.printStackTrace();
			}
		}
		
		System.out.println("Done.");

	}


}
