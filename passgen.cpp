#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>   
using namespace std;

//SE GENERATA PIU' DI UNA PASS, FUNZIONE PER SCEGLIERE LA PIU' SICURA

string passGen(bool symbs, bool numbs, int len, bool upper){
    string pass = "";
    for(int i = 0; i < len; i++){
        char c;
        if(symbs && upper && numbs){
            c = (rand()% (126 - 33 + 1)) + 33;
        }
        else if(symbs && numbs){
            do{
                c = (rand()% (126 - 33 + 1)) + 33;
            }while(c >= 65 && c <= 90);
        }
        else if(symbs){
            do{
                c = (rand()% (126 - 33 + 1)) + 33;
            }while((c >= 65 && c <= 90) || (c >=48 && c <= 57));
        }
        else if(numbs){
            c = rand()%(57-48+1)+48;
        }
        else if(upper){
            c = rand()&(90-65+1)+65;
        }
        else if(upper && symbs){
            do{
                c = (rand()% (126 - 33 + 1)) + 33;
            }while(c >= 48 && c <= 57);
        }
        else if(numbs && upper){
            do{
                c = (rand()% (122 - 48 + 1)) + 48;
            }while((c >= 58 && c <= 64) || (c >=91 && c<=96));
        }
        else{
            c = (rand()% (122 - 97 + 1)) + 97;
        }
        pass+=c;
    }
    return pass;
}

string passSec(vector<string>& pass){
    /*
        Punti sicurezza: ogni simbolo vale 35 pt, len*20 pt lunghezza, ogni numero 5 pt, ogni minuscola 10pt, ogni maiuscola 15pt.
        La password con il punteggio più alto è la più sicura.
    */
    string mst_Sec;
    int max_pts = 0;
    for(int i = 0; i < pass.size(); i++){
        int pts = pass[i].length()*20;
        for(int j = 0; j < pass[i].length(); j++){
            if(pass[i][j] >= 48 && pass[i][j] <= 57)
                pts+=5;
            else if(pass[i][j] >= 65 && pass[i][j] <= 90)
                pts+=15;
            else if(pass[i][j] >= 97 && pass[i][j] <= 122)
                pts+=10;
            else
                pts+=35;
        }
        if(max_pts < pts){
            max_pts = pts;
            mst_Sec = pass[i];
        }
    }
    return mst_Sec;

}



int main(){
    srand(time(0));
    bool symbs, numbs = 0, upper, sec, exit = 0;
    vector<string> pass;
    int len;
    while(!exit){
        do{
            cout << "Inserisci lunghezza password" << endl;
            cin >> len;
        }while(len <= 0);

        do{
            cout << "Vuoi generare un codice PIN?(1 = Y/0 = N)" << endl;
            cin >> numbs;
        }while(numbs != 1 && numbs != 0);

        if(numbs){
            cout << "Generazione Codice PIN" << endl;
            string pin = passGen(0, 1, len, 0);
            cout << "Codice PIN: " << pin << endl;
        }

        else{
            cout << "Si e' scelto di generare una Password convenzionale..." << endl;
            do{
                cout << "Caratteri speciali?(1 = Y/0 = N)" << endl;
                cin >> symbs;
            }while(symbs != 1 && symbs != 0);

            do{
                cout << "Lettere maiuscole?(1 = Y/0 = N)" << endl;
                cin >> upper;
            }while(upper != 1 && upper != 0);

            do{
                cout << "Numeri?(1 = Y/0 = N)" << endl;
                cin >> numbs;
            }while(numbs != 1 && numbs != 0);

            if(pass.size() >= 1){
                do{
                    cout << "Il programma sceglie per te la password piu' sicura? (1 = Y/0 = N)" << endl;
                    cin >> sec;
                }while(sec != 1 && sec != 0);
            }

            pass.push_back(passGen(symbs, numbs, len, upper));

            cout << pass[pass.size()-1] << endl;

            string secPass;
            if(sec){
                secPass = passSec(pass);
                cout << "La password piu' sicura e' " << secPass << endl;
            }
        }

        do{
            cout << "Generare un'altra password? (0 = Y / 1 = N) " << endl;
            cin >> exit;
        }while(exit != 0 && exit != 1);

    }
    return 0;

}