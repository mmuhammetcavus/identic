    First I implemented argparse arguments. I kept them as simple as I can because I didn't know about it much but I handled required conditions later 
on with simple if and else clauses.After that I created 6 global dictionaries variables (mapFiles, mapDirs etc..).With first 4 of them I kept hash 
values and list of paths which have that same hash value. 4 separate dictionaries were used to keep files because to keep directories and -n,-c options
separately. Last 2 dictionaries are used for directories and files sizes separately,and kept path with its size. Then I wrote 3 functions for -c , -n 
and -s arguments solutions. They were pretty straightforward with basic recursion. In them, I  simply matched paths with their hash value or sizes. Then 
in printPaths function first I executed 3 functions, those mentioned above, no matter what argument was given(-c or -n etc..). Later I realized that was
not efficient for best cases, but in the worst case I was gonna execute all that 3 functions anyway. So I decided left the code as it was. After 
executions of solution functions I just printed values that are in global dictionary variables and finalized the code.
