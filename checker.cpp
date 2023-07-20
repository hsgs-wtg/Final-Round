#include<bits/stdc++.h>
using namespace std;

const int PIPELINE_COUNT = 1;
const int SHIFT_COUNT = 28*3;
const int REQUIREMENT_COUNT = 3;
const int TASK = 1;

struct pipeline{
    vector<vector<vector<bool>>> x;
    vector<vector<bool>> A;
    vector<vector<int>> r;
    void read_number_of_people(){
        ifstream in("data/duLieu" + to_string(TASK) + "01_nhan_su.txt");
        int n = 0;
        string str;
        getline(in, str);
        while(in >> str){
            in >> str;
            n++;
        }
        x.resize(n);
        for(auto &vec: x){
            vec.resize(SHIFT_COUNT);
            for(auto &vec2: vec){
                vec2.resize(REQUIREMENT_COUNT);
            }
        }
        A.resize(n);
        for(auto &vec: )
    }
    void read_requirement(){

    }
    void read_schedule(){

    }
    void read_skills(){

    }
    void read_input(){

    }
}

int main(){

}