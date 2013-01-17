#include <math.h>
#include <stdlib.h>

#define kE 2.71828182846

typedef struct {
    int width;
    int height;
    double threshold;
    double influence;
    double *weights;
    double *values;
} Model;

double f(double x) {
    return 1.0 - pow(kE, -x);
}

double g(double y) {
    return y < 1.0 ? log(1.0 / (1.0 - y)) : 50.0;
}

int update(Model *model, double dt) {
    int result = 0;
    int width = model->width;
    int height = model->height;
    int count = width * height;
    double threshold = model->threshold;
    double influence = model->influence;
    double *weights = model->weights;
    double *values = model->values;
    while (dt > 0) {
        double d = dt;
        for (int i = 0; i < count; i++) {
            double e = (g(threshold) - g(values[i])) / weights[i];
            if (e < d) {
                d = e;
            }
        }
        dt -= d;
        for (int i = 0; i < count; i++) {
            values[i] = f(g(values[i]) + d * weights[i]);
        }
        int *seen = (int *)calloc(count, sizeof(int));
        while (1) {
            int done = 1;
            for (int i = 0; i < count; i++) {
                if (seen[i] || values[i] < threshold) {
                    continue;
                }
                seen[i] = 1;
                int x1 = i % width;
                int y1 = i / width;
                for (int j = 0; j < count; j++) {
                    if (seen[j] || i == j || values[j] >= threshold) {
                        continue;
                    }
                    done = 0;
                    int x2 = j % width;
                    int y2 = j / width;
                    int dx = abs(x2 - x1);
                    int dy = abs(y2 - y1);
                    int d2 = dx * dx + dy * dy;
                    values[j] += influence / d2;
                }
            }
            if (done) {
                break;
            }
        }
        free(seen);
        int n = 0;
        for (int i = 0; i < count; i++) {
            if (values[i] >= threshold) {
                values[i] = 0.0;
                n++;
            }
        }
        if (n > result) {
            result = n;
        }
    }
    return result;
}
