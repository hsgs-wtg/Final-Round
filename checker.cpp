#include<bits/stdc++.h>
using namespace std;

const int SHIFT_COUNT = 28*3;
const int REQUIREMENT_COUNT = 3;

const int TASK = 1;
const int PIPELINE_COUNT = 1;
const string SUBTASK = "a";

const string FILE_DIR = "data/duLieu" + to_string(TASK) + "/";
const string RESULT_DIR = "result/";

const int MAX_WORK_DAY = 24;

const string JOBS[3] = {"Rot", "May_dong_hop", "Pallet"};

map<string, int> JOB_INDEX = {
    {"Rot", 0},
    {"May_dong_hop", 1},
    {"Pallet", 2}
};

const int TIME_FRAME[3] = {6, 14, 22};

struct Pipeline{
    vector<vector<vector<vector<bool>>>> x;
    vector<vector<vector<bool>>> A;
    vector<vector<int>> r;
    vector<vector<int>> Q;
    void read_number_of_people(){
        ifstream cin(FILE_DIR + "01_nhan_su.txt");

        int n = 0;
        string str;
        getline(cin, str);
        while(cin >> str){
            cin >> str;
            n++;
        }

        x.resize(n);
        for(auto &vec: x){
            vec.resize(SHIFT_COUNT);
            for(auto &vec2: vec){
                vec2.resize(PIPELINE_COUNT);
                for(auto &vec3: vec2){
                    vec3.assign(REQUIREMENT_COUNT, 0);
                }
            }
        }

        A.resize(n);
        for(auto &vec: A){
            vec.resize(PIPELINE_COUNT);
            for(auto &vec2: vec){
                vec2.assign(REQUIREMENT_COUNT, 0);
            }
        }

        cin.close();
    }
    void read_requirement(){

        r.resize(PIPELINE_COUNT);
        for(auto &vec: r)vec.resize(REQUIREMENT_COUNT);

        ifstream cin(FILE_DIR + "02_dinh_bien.txt");
        string str;

        for(int i = 0; i < PIPELINE_COUNT; i++){
            for(int j = 0; j < REQUIREMENT_COUNT; j++){
                cin >> str;
                cin >> str;
                cin >> r[i][j];
            }
        }

        cin.close();
        
    }
    void read_schedule(int index){

        string f = (FILE_DIR + "lenh_san_xuat_Day_chuyen_" + to_string(index+1) + ".txt");
        const char* filename = f.c_str();
        FILE* ptr = fopen(filename, "r");
        char str[40];
        fgets(str, sizeof(str), ptr);

        Q.resize(SHIFT_COUNT);

        int yy, mm, dd, hh, mn, ss;
        while(fscanf(ptr, "%d-%d-%d %d:%d:%d; ", &yy, &mm, &dd, &hh, &mn, &ss) > 0){
            int l = (dd - 2)*3 + 2;
            for(auto v: TIME_FRAME)l += (hh >= v);
            fscanf(ptr, "%d-%d-%d %d:%d:%d", &yy, &mm, &dd, &hh, &mn, &ss);
            int r = (dd-2)*3+2;


            for(auto v: TIME_FRAME)r += (hh > v);
            for(int i = l; i <= r; i++){
                Q[i].push_back(index);
            }

            //cout << "Schedule: " << index << " " << l << " " << r << endl;
        }


        fclose(ptr);
    }
    void read_skills(int index, int job){
        string f = FILE_DIR + "ky_nang_Day_chuyen_" + to_string(index+1) + "_" + JOBS[job] + ".txt";
        const char* filename = f.c_str();
        FILE* ptr = fopen(filename, "r");
        
        int id;

        while(fscanf(ptr, "V%d\n", &id) > 0){
            //cout << "V" << id << " " << index << " " << job << "\n";
            A[id-1][index][job] = 1;
        }

        fclose(ptr);
        
    }
    //

    bool check_suitable_job(){
        bool good = true;
        for(int i = 0; i < x.size(); i++){
            for(int j = 0; j < SHIFT_COUNT; j++){
                for(int k = 0; k < PIPELINE_COUNT; k++){
                    for(int l = 0; l < REQUIREMENT_COUNT; l++){
                        if(x[i][j][k][l] > A[i][k][l]){
                            //cout << i << " " << j << " " << k << " " << l << endl;
                            good = false;
                        }
                    }
                }
            }
        }
        return good;
    }

    bool check_night_shift(){
        for(int i = 0; i < x.size(); i++){
            for(int j = 2; j+1 < SHIFT_COUNT; j+=3){
                int sum = 0;
                for(int k = 0; k < PIPELINE_COUNT; k++){
                    for(int l = 0; l < REQUIREMENT_COUNT; l++){
                        sum += x[i][j][k][l] + x[i][j+1][k][l];
                    }
                }
                if(sum > 1)return false;
            }
        }
        return true;
    }

    bool check_one_shift(){
        for(int i = 0; i < x.size(); i++){
            for(int j = 0; j+2 < SHIFT_COUNT; j+=3){
                int sum = 0;
                for(int k = 0; k < PIPELINE_COUNT; k++){
                    for(int l = 0; l < REQUIREMENT_COUNT; l++){
                        sum += x[i][j][k][l] + x[i][j+1][k][l] + x[i][j+2][k][l];
                    }
                }
                if(sum > 1)return false;
            }
        }
        return true;
    }

    bool check_24_days(){
        for(int i = 0; i < x.size(); i++){
            int sum = 0;
            for(int j = 0; j < SHIFT_COUNT; j++){
                for(int k = 0; k < PIPELINE_COUNT; k++){
                    for(int l = 0; l < REQUIREMENT_COUNT; l++){
                        sum += x[i][j][k][l];
                    }
                }
            }
            if(sum > MAX_WORK_DAY){
                cout << i << endl;
                return false;
            }
        }
        return true;
    }

    bool check_cardinality(){
        for(int j = 0; j < SHIFT_COUNT; j++){
            for(int k = 0; k < Q[j].size(); k++){
                for(int l = 0; l < REQUIREMENT_COUNT; l++){
                    int sum = 0;
                    for(int i = 0; i < x.size(); i++){
                        sum += x[i][j][Q[j][k]][l];
                    }
                    if(r[Q[j][k]][l] > sum)return false;
                }
            }
        }
        return true;
    }

    void read_input(){
        read_number_of_people();

        cout << "Finished reading number of people" << endl;

        read_requirement();

        cout << "Finished reading requirements" << endl;

        for(int i = 0; i < PIPELINE_COUNT; i++){
            read_schedule(i);
        }

        cout << "Finished reading schedule" << endl;
        
        for(int i = 0; i < PIPELINE_COUNT; i++){
            for(int j = 0; j < REQUIREMENT_COUNT; j++){
                read_skills(i, j);
            }
        }

        cout << "Finished reading skills" << endl;
    }

    void read_result(){

        int yy, mm, dd, shift, index, pipeline;

        char c[1000];        

        while(scanf("%d.%d.%d Ca_%d V%d Day_chuyen_%d %s", &dd, &mm, &yy, &shift, &index, &pipeline, c) > 0){
            string job(c);
            //cout << dd << endl;
            x[index-1][(dd - 1)*3 + shift - 1][pipeline-1][JOB_INDEX[job]] = 1;
        }
    }

    bool check(){
        bool good = true;

        if(!check_suitable_job()){
            cout << "Failed check: job not suitable" << endl;
            good = false;
        }
        
        if(!check_night_shift()){
            cout << "Failed check: worked after night shift" << endl;
            good = false;
        }

        if(!check_one_shift()){
            cout << "Failed check: worked more than one shift per day" << endl;
            good = false;
        }

        if(!check_24_days()){
            cout << "Failed check: worked more than 24 days" << endl;
            good = false;
        }

        if(!check_cardinality()){
            cout << "Failed check: not enough worker" << endl;
            good = false;
        }
        return good;
    }

};

Pipeline pipeline;

int main(){
    pipeline.read_input();
    pipeline.read_result();
    cout << pipeline.check() << endl;
}