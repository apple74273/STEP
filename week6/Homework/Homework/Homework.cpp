#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <ctime>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <iomanip>
using namespace std;

class Solver {
    public:
        double minDistance = 1000000000;
        double initialDistance = 1000000000;
        vector<vector<double>> cities;
        vector<int> answer;
        
        //Start the process of solving
        int start() {
            /*for (int i = 0; i < 8; i++) {
                initialize();
                readInput(i);
                solve();
                writeOutput(i);
                cout << "Finished " << i << "th data!" << endl;
                cout << endl << "-----" << endl << endl;
            }*/

            // When testing for one particular test case
            
            int i = 7;
            initialize();
            readInput(i);
            solve();
            writeOutput(i);
            cout << "Finished " << i << "th data!" << endl;
            

            return 0;
        }

        //Initialize global variables
        void initialize() {
            minDistance = 1000000000;
            initialDistance = 1000000000;
            cities.clear();
            answer.clear();
        }

        //Call each methods to get the minimum distance
        void solve() {

            vector<int> initialTour = greedy();
            //vector<int> initialTour = createInitialTour(); //FOR TESTING

            if (initialTour.size() < 10) {
                initialTour = bruteForce(initialTour);
                answer = initialTour;
            } else {
                int clusterCount = 4;
                initialTour = annealing(initialTour);
                vector<vector<int>> dividedTour = divideTour(initialTour, clusterCount);

                for (int i = 0; i < dividedTour.size(); i++) {
                    dividedTour[i] = removeCross(dividedTour[i]); //TODO: cross-cluster
                    cout << "Finished removing crosses!" << endl;
                }

                for (int i = 0; i < dividedTour.size(); i++) {
                    for (int j = 0; j < dividedTour[i].size(); j++) {
                        answer.push_back(dividedTour[i][j]);
                    }
                }
            }
            return;
        }

        // dividing the tour into smaller clusters
        vector <vector<int>> divideTour(vector<int> initialTour, int clusterCount) {
            vector <vector <int>> dividedTour;
            if (cities.size() > 8000) {
                int length = initialTour.size() / clusterCount;
                length++;
                int index = 0;
                for (int i = 0; i < clusterCount; i++) {
                    vector<int> division;
                    for (int j = 0; j < length; j++) {
                        if (j == length - 1) {
                            if (initialTour.size() % clusterCount <= i) {
                                continue;
                            }
                        }
                        division.push_back(initialTour[index]);
                        index++;
                    }
                    dividedTour.push_back(division);
                }
            }
            else {
                dividedTour.push_back(initialTour);
            }

            return dividedTour;
        }

        // writing the answer as a csv file
        void writeOutput(int count) {
            answer.pop_back();

            ofstream file("output_" + to_string(count) + ".csv");
            file << "index" << endl;
            for (int i : answer) {
                file << i << endl;
            }
        }

        // reading input from csv file
        void readInput(int count) {
           ifstream file("input_" + to_string(count) + ".csv");
            string line;
            getline(file, line);  // Skip the header row
            while (getline(file, line)) {
                stringstream lineStream(line);
                string cell;
                vector<double> city;
                while (getline(lineStream, cell, ',')) {
                    city.push_back(stod(cell));
                }
                cities.push_back(city);
            }
        }

        // FOR TEST: creating a initial tour
        vector <int> createInitialTour() {
            int N = cities.size();
            vector<vector<double>> dist(N, vector<double>(N, 0));
            vector<int> tour;
            for (int i = 0; i < N; i++) {
                for (int j = i; j < N; j++) {
                    dist[i][j] = dist[j][i] = distance(cities[i], cities[j]);
                }
            }

            int currentCity = 0;
            tour = { currentCity };
            double distance = 0;

            for (int i = 1; i < N; i++) {
                int nextCity = i;
                distance += dist[currentCity][nextCity];
                tour.push_back(nextCity);
                currentCity = nextCity;
            }

            distance += dist[currentCity][tour[0]];
            tour.push_back(tour[0]);

            cout << "Finished creating initial tour!" << endl;
            return tour;
        }

        // creating an initial answer based on greedy technique
        vector<int> greedy() {
            int N = cities.size();
            vector<vector<double>> dist(N, vector<double>(N, 0));
            vector<int> tour;
            for (int i = 0; i < N; i++) {
                for (int j = i; j < N; j++) {
                    dist[i][j] = dist[j][i] = distance(cities[i], cities[j]);
                }
            }

            int currentCity = 0;
            vector<bool> unvisitedCities(N, true);
            unvisitedCities[0] = false;
            tour = { currentCity };
            double distance = 0;

            for (int i = 1; i < N; i++) {
                int nextCity = -1;
                double minDist = numeric_limits<double>::infinity();
                for (int j = 0; j < N; j++) {
                    if (unvisitedCities[j] && dist[currentCity][j] < minDist) {
                        nextCity = j;
                        minDist = dist[currentCity][j];
                    }
                }
                distance += minDist;
                unvisitedCities[nextCity] = false;
                tour.push_back(nextCity);
                currentCity = nextCity;
            }

            distance += dist[currentCity][tour[0]];
            tour.push_back(tour[0]);

            cout << "Finished greedy!" << endl;
            return tour;
        }

        // calculate a distance between the two points
        double distance(vector<double> city1, vector<double> city2) {
            return sqrt((city1[0] - city2[0]) * (city1[0] - city2[0]) + (city1[1] - city2[1]) * (city1[1] - city2[1]));
        }

        // simulated annealing
        vector<int> runAnnealing(double startTime, double timeLimit, vector<int> tour, int count) {
            random_device rd;
            mt19937 gen(rd());
            uniform_int_distribution<> dis(1, tour.size() - 2);

            int first = dis(gen);
            int second = dis(gen);

            if (first == second) {
                return tour;
            }

            pair<vector<int>, double> result = swapRoute(first, second, tour);
            vector<int> newTour = result.first;
            double newDistance = result.second;

            double randProb = static_cast<double>(rand()) / RAND_MAX;
            double probability = getProbability(startTime, timeLimit, newDistance);

            // FOR DEBUG:
            if (count % 50 == 0) {
                cout << probability << ", " << newDistance << ", " << minDistance << endl << setprecision(10);
            }
            
            //TODO: look up probability curve
            // Annealing1
            //本当はこっちにしたかったけど上手くいかなかった
            /*if (probability > randProb) {
                tour = newTour;
                minDistance = newDistance;
            }*/

            //Annealing2
            if (newDistance < minDistance) {
                tour = newTour;
                minDistance = newDistance;
            }

            return tour;
        }

        vector<int> annealing(vector<int> tour) {
            double startTime = static_cast<double>(clock()) / CLOCKS_PER_SEC;
            double timeLimit = 600;
            initialDistance = minDistance;
            int count = 0;
            while ((static_cast<double>(clock()) / CLOCKS_PER_SEC - startTime) < timeLimit) {
                tour = runAnnealing(startTime, timeLimit, tour, count);
                count += 1;
            }

            cout << "Finished simulated annealing!" << endl;

            return tour;
        }

        // swap two points inside the route
        pair<vector<int>, double> swapRoute(int first, int second, vector<int> tour) {
            vector<int> newTour(tour.size());
            copy(tour.begin(), tour.end(), newTour.begin());
            double newDistance = minDistance;

            double subtract1 = distance(cities[newTour[first]], cities[newTour[first + 1]]);
            double subtract2 = distance(cities[newTour[second]], cities[newTour[second + 1]]);
            double subtract3 = distance(cities[newTour[first]], cities[newTour[first - 1]]);
            double subtract4 = distance(cities[newTour[second]], cities[newTour[second - 1]]);

            swap(newTour[first], newTour[second]);

            double add1 = distance(cities[newTour[first]], cities[newTour[first + 1]]);
            double add2 = distance(cities[newTour[second]], cities[newTour[second + 1]]);
            double add3 = distance(cities[newTour[first]], cities[newTour[first - 1]]);
            double add4 = distance(cities[newTour[second]], cities[newTour[second - 1]]);

            newDistance -= (subtract1 + subtract2 + subtract3 + subtract4);
            newDistance += (add1 + add2 + add3 + add4);

            return make_pair(newTour, newDistance);
        }

        // calculate a probability for simulated annealing
        double getProbability(double startTime, double timeLimit, double newDistance) {
            if (newDistance < minDistance) {
                return 1.0;
            }
            double startTemp = initialDistance * 0.000015;
            double endTemp = initialDistance * 0.0000001;
            double temp = startTemp + (endTemp - startTemp) * ((double)clock() / CLOCKS_PER_SEC / (startTime + timeLimit));
            double probability = exp((minDistance - newDistance) / temp); //TODO: change function
            //FOR DEBUG:
            //cout << temp << ", " << probability << ", " << (minDistance - newDistance) << ", " << (minDistance-newDistance)/temp << endl;
            return probability;
        }

        // when the two lines intersect each other, reorganize the points so that there is no intersections
        vector<int> removeCross(vector<int> tour) {
            bool continueFlag = true;
            while (continueFlag) {
                continueFlag = false;
                int N = tour.size();
                for (int i = 1; i < N - 2; ++i) {
                    for (int j = i + 2; j < N - 1; ++j) {
                        if (judgeCross(i, j, tour)) {
                            pair<vector<int>, double> result = fixChain(i, j, tour);
                            tour = result.first;
                            double tempDistance = result.second;
                            if (tempDistance < minDistance) {
                                continueFlag = true;
                                minDistance = tempDistance;
                            }
                        }
                    }
                }
            }

            return tour;
        }

        // checking whether two lines (created by p1&p2 and p3&p4) has an intersection
        bool judgeCross(int i, int j, vector<int> tour) {
            vector<double> first = cities[tour[i]];
            vector<double> second = cities[tour[j]];
            vector<double> firstNext = cities[tour[i + 1]];
            vector<double> secondNext = cities[tour[j + 1]];

            // x座標による判定
            if (!maxMinCross(first[0], firstNext[0], second[0], secondNext[0])) {
                return false;
            }

            // y座標による判定
            if (!maxMinCross(first[1], firstNext[1], second[1], secondNext[1])) {
                return false;
            }

            double tc1 = (first[0] - firstNext[0]) * (second[1] - first[1]) + (first[1] - firstNext[1]) * (first[0] - second[0]);
            double tc2 = (first[0] - firstNext[0]) * (secondNext[1] - first[1]) + (first[1] - firstNext[1]) * (first[0] - secondNext[0]);
            double td1 = (second[0] - secondNext[0]) * (first[1] - second[1]) + (second[1] - secondNext[1]) * (second[0] - first[0]);
            double td2 = (second[0] - secondNext[0]) * (firstNext[1] - second[1]) + (second[1] - secondNext[1]) * (second[0] - firstNext[0]);
            return tc1 * tc2 <= 0 && td1 * td2 <= 0;
        }

        // checking whether x or y coordinates of two lines (created by p1&p2 and p3&p4) has an intersection
        bool maxMinCross(double p1, double p2, double p3, double p4) {
            double minab = min(p1, p2);
            double maxab = max(p1, p2);
            double mincd = min(p3, p4);
            double maxcd = max(p3, p4);

            if (minab > maxcd || maxab < mincd) {
                return false;
            }

            return true;
        }

        // changing the order of the tour and re-calculate the distance of the given two points
        pair<vector<int>, double> fixChain(int start, int end, vector<int> tour) {
            vector<int> newTour(tour.size());
            copy(tour.begin(), tour.end(), newTour.begin());
            double newDistance = 0;
            for (int i = 0; i < end - start; ++i) {
                newTour[start + i + 1] = tour[end - i];
            }

            int N = tour.size();

            for (int i = 0; i < N - 1; ++i) {
                newDistance += distance(cities[newTour[i]], cities[newTour[i + 1]]);
            }

            return make_pair(newTour, newDistance);
        }

        // do brute-force method if the number of cities is small
        vector<int> bruteForce(vector<int> tour) {
            vector<bool> visited(tour.size(), false);
            visited[0] = true;
            int countVisited = 1;
            double nowDistance = 0;
            vector<int> nowTour = { 0 };
            tour = runBruteForce(nowTour, nowDistance, 0, visited, countVisited, tour);
            cout << "Finished brute force!" << endl;
            return tour;
        }

        vector<int> runBruteForce(vector<int> nowTour, double nowDistance, int nowPlace, vector<bool> visited, int countVisited, vector<int> tour) {
            if (countVisited == tour.size()-1) {
                nowDistance += distance(cities[nowPlace], cities[0]);
                nowTour.push_back(0);
                if (nowDistance < minDistance) {
                    tour = nowTour;
                    minDistance = nowDistance;
                }
                return tour;
            }

            vector<int> newTour(nowTour.size());
            copy(nowTour.begin(), nowTour.end(), newTour.begin());
            vector<bool> newVisited(visited.size());
            copy(visited.begin(), visited.end(), newVisited.begin());

            for (int i = 0; i < tour.size()-1; ++i) {
                if (visited[i]) continue;

                newVisited[i] = true;
                newTour.push_back(i);
                nowDistance += distance(cities[nowPlace], cities[i]);
                tour = runBruteForce(newTour, nowDistance, i, newVisited, countVisited + 1, tour);
                nowDistance -= distance(cities[nowPlace], cities[i]);
                newTour.pop_back();
                newVisited[i] = false;
            }

            return tour;
        }


};

int main() {
    Solver solver;
    solver.start();

    return 0;
}