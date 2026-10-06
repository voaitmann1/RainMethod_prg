#include <QCoreApplication>
#include<string>
#include<QDir>
#include<QStringList>
#include<windows.h>
#include<iostream>
#include<locale.h>
#include<qdebug.h>

const QString _InPath="C:\\temp\\FilesToSplit\\";
const QString _OutPath="C:\\temp\\FilesToSplit\\Splitted\\";


QStringList GetFileNamesByQt(const QString& path){
    QStringList files;
    QDir dir(path);
    if(!dir.exists()){
        return files;
    }
    return dir.entryList(QDir::Files | QDir::NoDotAndDotDot);
}

std::vector<std::wstring> GetFileNamesByWinAPI(const std::wstring& path){
    //std::vector<std::string>files;
    std::vector<std::wstring>files;

    WIN32_FIND_DATAW ffd;

    HANDLE hFind = FindFirstFileW((path+L"\\*").c_str(), &ffd);

    if(hFind==INVALID_HANDLE_VALUE){
        return files;
    }

    do{
        if(!(ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)){
            files.push_back(ffd.cFileName);
        }
    }

    while(FindNextFileW(hFind, &ffd));//what?

    FindClose(hFind);

    return files;
}

QString SplitFileNameToOneOf2Parts(const QString& fn_in, int N){
    QString fn_noExt, fnr="", sn;
    int inL=fn_in.size();
    fn_noExt=fn_in.mid(0, inL-4);
    if(inL>0 && N>=1 && N<=2){
        sn.setNum(N);
        fnr=_OutPath+fn_noExt+"_part"+sn+".txt";
    }
    return fnr;
}

void SplitFile(char*fname2x1){
    FILE *f2x1, *f1of1, *f2of1;
    float num1, num2;
    char *fname1of1, *fname1of2;
    std::string s_fname2x1,   s_fname1of1,   s_fname2of1,
                s_nmNoExt1x2, s_nmNoExt1of1, s_nmNoExt2of1,
                s_ext1x2,     s_ext1of1,     s_ext2of1;
    int         L_fname2x1,   L_fname1of1,   L_fname2of2,
                L_nmNoExt1x2, L_nmNoExt1of1, L_nmNoExt1of2,
                L_ext1x2,     L_ext1of1,     L_ext2of1,
       countVals=0;
    f2x1=fopen(fname2x1, "r");
    if(f2x1!=NULL){
        s_fname2x1=std::string(fname2x1);
        L_fname2x1=s_fname2x1.size();
        //s_nmNoExt1x2=s_fname2x1.erase(s_fname2x1.begin()+L_fname2x1-1-4, 4);
        s_nmNoExt1x2=s_fname2x1.erase(L_fname2x1-4, 4);
        s_nmNoExt1of1=s_nmNoExt1x2+"_1of1";
        s_nmNoExt2of1=s_nmNoExt1x2+"_2of1";
        s_fname1of1=s_nmNoExt1of1+".txt";
        s_fname2of1=s_nmNoExt2of1+".txt";
        f1of1=fopen(s_fname1of1.c_str(), "w");
        f2of1=fopen(s_fname2of1.c_str(), "w");
        while(!feof(f2x1)){
            fscanf(f2x1, "%f%f\n", &num1, &num2);
            fprintf(f1of1, "%f\n", num1);
            fprintf(f2of1, "%f\n", num2);
            countVals++;
        }
        fclose(f2x1);
        fclose(f1of1);
        fclose(f2of1);
    }
}

bool SplitFile(
    const QString& inName,
    const QString& out1Name,
    const QString& out2Name
    )
{
    QFile fin(inName);
    QFile fout1(out1Name);
    QFile fout2(out2Name);

    //
    //wstring ws;
    //inName.fromStdWString(ws);
    //

    bool b=true;

    if(!fin.open(QIODevice::ReadOnly | QIODevice::Text)){
        printf("Problems with File In \n");
        //wprintf(L"%ls\n",ws.c_str());
        wprintf(L"file: %ls\n",inName.toStdWString().c_str());
        //std::cout<<inName.toStdWString().c_str()<<std::endl;
        //return false;
        b=false;
    }
    if(!fout1.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        fin.close();
        printf("Problems with File Out1\n");
        //return false;
        b=false;
    }

    if(!fout2.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        fin.close();
        fout1.close();
        printf("Problems with File Out2\n");
        //return false;
        b=false;
    }

    if(b==false){
        return b;
    }

    QTextStream in(&fin);
    QTextStream out1(&fout1);
    QTextStream out2(&fout2);

    double x, y;

    while(!in.atEnd())
    {
        in >> x >> y;

        if(in.status() != QTextStream::Ok)
            break;

        out1 << x << "\n";
        out2 << y << "\n";
    }

    fin.close();
    fout1.close();
    fout2.close();

    return true;
}

enum FileElaborationMode {i_WinAPI, i_Qt};

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    setlocale(LC_ALL,"");

    //int modeN=2;
    FileElaborationMode modeN=i_WinAPI;
    int QOfFiles;

    bool FileElaboratedWell;

    std::vector<std::wstring>fileNames1;
    QStringList fileNames2;
    std::wstring ws;
    QString qs;
    std::wstring path=_InPath.toStdWString();//L"C:\\temp\\FilesToSplit";
    //fileNames=GetFileNamesByWinAPI(L"C:\\temp\\FilesToSplit");
    fileNames1=GetFileNamesByWinAPI(path);
    fileNames2=GetFileNamesByQt(qs=QString::fromStdWString(path));
    //
    if(modeN==i_WinAPI){
        QOfFiles=fileNames1.size();
        for(int i=0; i<QOfFiles; i++){
            ws=fileNames1[i];
            qs=QString::fromStdWString(ws);
            printf("%d) L= %d\n",i+1, ws.length());
            wprintf(L"%ls\n",ws.c_str());
            //qDebug()<<qs<<"  !!  ";//invalid use of incomplete class
            //printf("%s\n",qs.toStdString().c_str());
            //wprintf(L"%ls\n",qs.toStdWString().c_str());
            //std::wcout<<ws;
            //std::wcout<<ws.c_str();
            //std::cout<<std::endl;
        }
        for(int i=0; i<QOfFiles; i++){
            //if(i==10)
            //{
                ws=fileNames1[i];
                qs=QString::fromStdWString(ws);
                FileElaboratedWell=SplitFile(QString::fromStdWString(path)+"\\"+qs, SplitFileNameToOneOf2Parts(qs, 1), SplitFileNameToOneOf2Parts(qs, 2));
                if(FileElaboratedWell){
                    //printf("\nSplitted successfully\n");
                }else{
                    printf("\nPrpblems occured while splitting file\n");
                }
                //if(FileElaboratedWell){
                //    printf("\nSplitted successfully\n");
                //}else{
                //    printf("\nPrpblems occured while splitting file\n");
                //}
            //}
        }
        printf("all files elaborated\n");
    }else if(modeN==i_Qt){
         QOfFiles=fileNames2.size();
         for(int i=0; i<QOfFiles; i++){
             //qs=fileNames2.at(i);
             ws=fileNames2.at(i).toStdWString();
             qs=QString::fromStdWString(ws);
             printf("%d) L= %d\n",i+1, ws.length());
             wprintf(L"%ls\n",ws.c_str());
         }
         for(int i=0; i<QOfFiles; i++){
             if(i==11)
             {
             qs=fileNames2.at(i);
             FileElaboratedWell=SplitFile(qs, SplitFileNameToOneOf2Parts(qs, 1), SplitFileNameToOneOf2Parts(qs, 2));
             }
         }
    }
    //for(int i=0; i<QOfFiles; i++){
    //    ws=fileNames[i];
    //}

    return a.exec();
}

