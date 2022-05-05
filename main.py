import os
import mel_parser


def main():
    prog = '''
    void foo();
    
    int main(map m, bool g)
    {
        int test_multimap = m[12][23];
        
        int a = 0;
        int g, g2 = g, g = 90;
        
        int temp = 24;
        
        if (42 in m)
            temp = m[42];

        if (g > 89)
            output(temp);
            
        while (c > 10)
            c = c - 1;

        a = input(); b = input();  /* comment 1
        c = input();
        */
        for (int i = 0, j = 8; ((i <= 5)) && g; i = i + 1, print(5))
            for(; a < b;)
                if (a > 7 + b) {
                    c = a + b * (2 - 1) + 0;  // comment 2
                    b = "42\t451";
                }
                else if (f)
                    output(c + 1, 89.89);
    }
    '''
    prog = mel_parser.parse(prog)
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
