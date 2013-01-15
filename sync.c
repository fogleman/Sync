#include <math.h>
#include <stdlib.h>

#define kE 2.71828182846

typedef struct {
    int size;
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

void update(Model *model, double dt) {
    int n = model->size;
    int count = n * n;
    int m = 4;
    double *values = (double *)calloc(count, sizeof(double));
    for (int i = 0; i < count; i++) {
        model->values[i] += dt;
        values[i] = model->values[i];
    }
    for (int i = 0; i < count; i++) {
        if (f(values[i]) < model->threshold) {
            continue;
        }
        int x1 = i % n;
        int y1 = i / n;
        for (int j = 0; j < count; j++) {
            if (i == j) {
                continue;
            }
            int x2 = j % n;
            int y2 = j / n;
            int dx = abs(x2 - x1);
            int dy = abs(y2 - y1);
            if (dx > m || dy > m) {
                continue;
            }
            int d2 = dx * dx + dy * dy;
            model->values[j] =
                g(f(model->values[j]) + model->influence / d2);
        }
    }
    for (int i = 0; i < count; i++) {
        if (f(values[i]) >= model->threshold) {
            model->values[i] = 0.0;
        }
    }
    free(values);
}
