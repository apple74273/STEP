import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Main {
	List<Pair> dictionary = new ArrayList<Pair>();
    public static void main(String[] args) {
    	Homework1 homework1 = new Homework1();
    	homework1.solve();
    }
    
    void solve() {
    	createDictionary(); //辞書の作成
    	String target = getInput(); //アナグラムを受け取る
    	printAnswer(target); //解答となる単語を出力
    }
    
    String getInput() {
    	//入力の受け取り
    	Scanner sc = new Scanner (System.in);
    	String target = sc.next();
    	sc.close();
    	return target;
    }
    
    void printAnswer(String target) {
    	//受け取ったアナグラムに対応する単語を出力
    	char[] targetAlphabet = target.toCharArray();
    	Arrays.sort(targetAlphabet);
    	String sortedTarget = new String (targetAlphabet);
    	Pair targetPair = new Pair (sortedTarget, sortedTarget);
    	int index = ~Collections.binarySearch(dictionary, targetPair, (a, b) -> a.sortedWord.compareTo(b.sortedWord) >= 0 ? 1 : -1);
    	
    	int answerCount = 0;
    	while(index<dictionary.size()) {
    		Pair pair = dictionary.get(index);
    		if (pair.sortedWord.equals(sortedTarget)) {
    			System.out.println(pair.word);
    			index++;
    			answerCount++;
    		} else {
    			break;
    		}
    	}
    	System.out.println("find "+answerCount+" word(s)!"); //対応する単語がゼロの場合でも終了を分かりやすくするため
    }
    
    void createDictionary() {
    	//辞書の作成
    	try {
    		Path path = Paths.get("C:\\Users\\na742\\eclipse-workspace\\atcoderJava\\src\\atcoderJava\\words.txt");
			List<String> lines = Files.readAllLines(path);
			
			for (String word: lines) {
				char[] wordAlphabet = word.toCharArray();
				Arrays.sort(wordAlphabet);
				String sortedWord = new String (wordAlphabet);
				Pair pair = new Pair (word, sortedWord);
				dictionary.add(pair);
			}
			
			dictionary.sort((a, b) -> a.sortedWord.compareTo(b.sortedWord));
    	} catch(IOException ioex) {
			ioex.printStackTrace();
		}
    }
}

class Pair{
	//単語と、構成するアルファベットをソートしたものを紐づけるためのクラス
	String word;
	String sortedWord;
	
	public Pair(String word, String sortedWord) {
		this.word = word;
		this.sortedWord = sortedWord;
	}
}