import os
import mel_parser
import program


def main():
    prog = '''
    //void foo();
    
    int main(map<int, int> m, bool g1)
    {
        if (1 > 0) {
            int y = 1;     
        }
        else int y = 0;
        
        
        int a = 0;
        int g2, g = 90;
        
        map<int, int> m1;
        
        int temp = 24;
        
        if (42 in m)
            temp = m1[42];
            temp = 8;
            
        //if (g > 89)
        //     output(temp);
        
        int c = 100;
        int b = 7;
        
        while (c > 10)
            c = c % 1;

        //a = input(); b = input(); 
      /* comment 1
        //c = input();
        */
        for (int i = 0, j = 8; ((i <= 5)) && g; i = i + 1)
            for(; a < b;)
                if (a > 7 + b) {
                    c = a + b * (2 - 1) + 0;  // comment 2
                    //b = "42\t451";
                }
                //else c = 0;
                    //output(c + 1, 89.89);
        return a;
    }
    '''
    program.execute(prog)

    # prog = mel_parser.parse(prog)
    # print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
