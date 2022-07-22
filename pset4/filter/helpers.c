#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int rgbt_average;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Average of the color values
            rgbt_average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = rgbt_average;

        }
    }
    return;
}


// Keeping whole numbers between 0 and 255
int cap(int rgbt)
{
    return rgbt > 255 ? 255 : rgbt;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            // Algorithm for converting an image to sepia

            image[i][j].rgbtRed = cap(round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue));
            image[i][j].rgbtGreen = cap(round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue));
            image[i][j].rgbtBlue = cap(round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue));
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];  // Create temporary variable to swap pixel values

    for (int i = 0; i < height; i++)
    {
        int spot = 0;
        for (int j = width - 1; j >= 0; j--, spot++)
        {
            temp[i][spot] = image[i][j];
        }

    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];  // creating temporary array

    // Reading color values of neighboring pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumR = 0;
            int sumG = 0;
            int sumB = 0;
            float count = 0.0;

            for (int m = -1; m < 2; m++)
            {
                for (int n = -1; n < 2; n++)
                {
                    if (i + m < 0 || i + m > height - 1 || j + n < 0 || j + n > width - 1)
                    {
                        continue;
                    }
                    //Calculation of around pixels summation
                    sumR += image[i + m][j + n].rgbtRed;
                    sumG += image[i + m][j + n].rgbtGreen;
                    sumB += image[i + m][j + n].rgbtBlue;
                    count++;

                }

            }
            //Copy average color value of neighboring pixels to temp array
            temp[i][j].rgbtBlue = round(sumB / count);
            temp[i][j].rgbtGreen = round(sumG / count);
            temp[i][j].rgbtRed = round(sumR / count);


        }
    }

    //Update new values of blurring pixels
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    return;

}
