
#include <cuda_runtime.h>   
#include<iostream>
using namespace std;
#include <fstream>

__global__ void mandelbrot(int* output, int width, int height,
                           int max_iter,
                           float x_min, float x_max,
                           float y_min, float y_max) {

    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if(x>= width || y>=height){
        return;
    }
    float cx = x_min + (static_cast<float>(x) / (width - 1))* (x_max - x_min);
    float cy = y_min + (static_cast<float>(y) / (height - 1))* (y_max - y_min);


    float zx = 0.0f;
    float zy = 0.0f;    
    
    bool escaped = false;

    for (int i = 0; i < max_iter; i++) {
    

        float new_zx = zx * zx - zy * zy + cx;
        float new_zy = 2.0f * zx * zy + cy;

        zx = new_zx;
        zy = new_zy;

        if(zx*zx + zy*zy > 4){
            int pixel_ind = y * width + x;
            escaped = true;
            output[pixel_ind] = i;
            break;
        }
    
    }
    if(!escaped){
        int pixel_ind = y * width + x;
        output[pixel_ind] = max_iter;
    }
    
}

int main() {
    int width = 800;
    int height = 600;
    int max_iter = 100;

    float x_min = -2.5f;
    float x_max = 1.0f;
    float y_min = -1.25f;
    float y_max = 1.25f;

    int total_pixels = width * height;
    size_t bytes = total_pixels * sizeof(int);

    int* h_output = new int[total_pixels];
    int* d_output = nullptr;
    cudaError_t err = cudaMalloc(&d_output, bytes);

    if (err != cudaSuccess) {
        std::cerr << "cudaMalloc failed: "
                  << cudaGetErrorString(err) << '\n';
        delete[] h_output;
        return 1;
    }

    dim3 block(16, 16);
    dim3 grid(
        (width + block.x - 1) / block.x,
        (height + block.y - 1) / block.y
    );

    cudaEvent_t start, stop;

    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);


    mandelbrot<<<grid, block>>>(
        d_output, width, height, max_iter,
        x_min, x_max, y_min, y_max
    );

    cudaEventRecord(stop);
cudaEventSynchronize(stop);

float milliseconds = 0.0f;
cudaEventElapsedTime(&milliseconds, start, stop);

cout << "CUDA kernel time: " << milliseconds << " ms\n";

cudaEventDestroy(start);
cudaEventDestroy(stop);

    err = cudaGetLastError();

    if (err == cudaSuccess) {
        err = cudaDeviceSynchronize();
    }

    if (err != cudaSuccess) {
        cerr << "Kernel failed: "
                  << cudaGetErrorString(err) << '\n';
        cudaFree(d_output);
        delete[] h_output;
        return 1;
    }
    err = cudaMemcpy(
        h_output, d_output, bytes, cudaMemcpyDeviceToHost
    );

    
    

    if (err != cudaSuccess) {
        cerr << "cudaMemcpy failed: "
                  << cudaGetErrorString(err) << '\n';
        cudaFree(d_output);
        delete[] h_output;
        return 1;
    }

    ofstream file("iterations.bin", std::ios::binary);

    file.write(
        reinterpret_cast<char*>(h_output),
        total_pixels * sizeof(int)
    );

    file.close();
    cout << "Saved iterations.bin\n";

    

    cudaFree(d_output);
    delete[] h_output;

    return 0;
}