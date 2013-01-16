#include <math.h>
#include <stdlib.h>

#define kE 2.71828182846

typedef struct {
    int width;
    int height;
    double threshold;
    double influence;
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
    double xt = g(model->threshold);
    while (dt > 0) {
        double mini = 0;
        double mind = xt - model->values[0];
        for (int i = 1; i < count; i++) {
            double d = xt - model->values[i];
            if (d < mind) {
                mini = i;
                mind = d;
            }
        }
        double d = mind < dt ? mind : dt;
        dt -= d;
        for (int i = 0; i < count; i++) {
            model->values[i] += d;
        }
        int *seen = (int *)calloc(count, sizeof(int));
        while (1) {
            int done = 1;
            for (int i = 0; i < count; i++) {
                if (seen[i] || model->values[i] < xt) {
                    continue;
                }
                done = 0;
                seen[i] = 1;
                int x1 = i % width;
                int y1 = i / width;
                for (int j = 0; j < count; j++) {
                    if (seen[j] || i == j) {
                        continue;
                    }
                    int x2 = j % width;
                    int y2 = j / width;
                    int dx = abs(x2 - x1);
                    int dy = abs(y2 - y1);
                    int d2 = dx * dx + dy * dy;
                    model->values[j] =
                        g(f(model->values[j]) + model->influence / d2);
                }
            }
            if (done) {
                break;
            }
        }
        free(seen);
        int n = 0;
        for (int i = 0; i < count; i++) {
            if (model->values[i] >= xt) {
                model->values[i] = 0.0;
                n++;
            }
        }
        if (n > result) {
            result = n;
        }
    }
    return result;
}
