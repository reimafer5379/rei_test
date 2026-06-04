#include <bits/stdc++.h>
#include <iostream>

using namespace std;   

int main()
{
    unsigned int n;
    cin >> n;

    int matrix [n][n];
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < n; k++)
        {
            int ik_el;
            cin >> ik_el;
            matrix[i][k] = ik_el;
        }
    }

    vector <pair<int, int>> lines;
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < n; k++)
        {
            if (matrix[i][k] == 1)
            {
                lines.push_back({i, k});
            }
        }
    }

    cout << lines.size();
    return 0;
}