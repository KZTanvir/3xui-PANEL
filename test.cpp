#include<iostream>
using namespace std;

int main(){
    int n = 5;

    for(int i=0; i<n; i++){
        for(int j=i+1; j<n; j++){
            cout << ' ';
        }
        cout << '/';
        for(int j=0; j<i*2; j++){
            cout << '-';
        }
        cout << '\\' << endl;
    }
    for(int i=n-1; i>=0; i--){
        for(int j=i+1; j<n; j++){
            cout << ' ';
        }
        cout << '\\';
        for(int j=0; j<i*2; j++){
            cout << '-';
        }
        cout << '/' << endl;
    }
}