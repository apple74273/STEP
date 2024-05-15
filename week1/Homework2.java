import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Homework2 {
	
	List <Pair> dictionary = new ArrayList<Pair>(); 
	String  filePath = "./"; //Eclipse実行時はプロジェクトファイルからのパスに変更
    public static void main(String[] args) {

    	//辞書の長さ (N) は84903
    	//単語の長さは (M) 17-37文字 → 2^Mがすごく大きくなるね
    	
    	Homework2 homework2 = new Homework2();
    	homework2.solve();

    }
    
    void solve() {
    	createDictionary(); //辞書の作成
    	createAnswer(); //解答の作成
    }
    
    void createAnswer() {
    	//3種類のファイルそれぞれに対して解答ファイルを作成
    	String[] fileNames = {"small", "medium", "large"};
    	for (int i=0; i<3; i++) {
    		List<String> wordsList = getList(fileNames[i]);
    		List <String> answerList = new ArrayList<String>();
    		//解答リストの作成
    		for (int j=0; j<wordsList.size(); j++) {
    			String answer = findWord(wordsList.get(j));
    			answerList.add(answer);
    		}
    		createFile(answerList, fileNames[i]);
    	}
    }
    
    void createFile(List<String> answerList, String name) {
    	//解答リストをテキストファイルに出力
    	try {
    		Path file = Paths.get(filePath+name+"_answer.txt");
    		Files.createFile(file);
    		FileWriter fw = new FileWriter(filePath+name+"_answer.txt");
    		PrintWriter pw = new PrintWriter(new BufferedWriter(fw));
    		for (int i=0; i<answerList.size(); i++) {
    			pw.println(answerList.get(i));
    		}
    		pw.close();
    	}  catch(IOException ioex) {
			ioex.printStackTrace();
		}
    }
    List <String> getList (String name){
    	List <String> list = new ArrayList<String>();
    	try {
			Path path = Paths.get(filePath+name+".txt");
			List<String> lines = Files.readAllLines(path);
			
			for (String word: lines) {
				list.add(word);
			}
    	} catch(IOException ioex) {
			ioex.printStackTrace();
		}
    	
    	return list;
    }
    
    String findWord(String target) {
    	//与えられたアナグラムで作れる単語を返す (複数ある場合は最もスコアが高い物を返す)
    	int[] scoreList = {1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4};
    	
    	Scanner sc = new Scanner (System.in);
    	int[] targetAlphabet = new int[26];
    	
    	for (int i=0; i<target.length(); i++) {
    		char a = target.charAt(i);
    		targetAlphabet[(int)(a-'a')]++;
    	}
    	
    	int maxScore = 0;
    	String maxWord = null;
    	for (int i=0; i<dictionary.size(); i++) {
    		Pair pair = dictionary.get(i);
    		int[] alphabet = pair.alphabet;
    		
    		boolean flag = true;
    		for (int j=0; j<26; j++) {
    			if (alphabet[j]>targetAlphabet[j]) {
    				flag = false;
    			}
    		}
    		
    		if (flag) {
    			String word = pair.word;
    			int score = 0;
    			for (int j=0; j<word.length(); j++) {
    				char a = word.charAt(j);
    				score += scoreList[(int)(a-'a')];
    			}
    			if (score>maxScore) {
    				maxScore = score;
    				maxWord = word;
    			}
    		}
    	}
    	sc.close();
    	return maxWord;
    }
    
    void createDictionary() {
    	//辞書を作成
    	try {
			Path path = Paths.get(filePath+"words.txt");
			List<String> lines = Files.readAllLines(path);
			
			for (String word: lines) {
				Pair pair = new Pair (word);
				dictionary.add(pair);
			}
    	} catch(IOException ioex) {
			ioex.printStackTrace();
		}
    }
}

class Pair{
	//単語と、その単語を構成するアルファベットを持つクラス
	String word;
	int[] alphabet;
	
	public Pair(String word) {
		this.word = word;
		this.alphabet = new int[26];
		for (int i=0; i<word.length(); i++) {
			char a = word.charAt(i);
			this.alphabet[(int)(a-'a')]++;
		}
	}
}