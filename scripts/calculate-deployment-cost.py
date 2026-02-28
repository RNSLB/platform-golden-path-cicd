#!/usr/bin/env python3
"""
Calculate estimated deployment cost
"""
import argparse
import sys

# Pricing (US East 1, 2026)
ECR_STORAGE_PER_GB = 0.10
GITHUB_ACTIONS_PER_MIN = 0.008
ECS_FARGATE_PER_VCPU = 0.04048
ECS_FARGATE_PER_GB = 0.004445
DATA_TRANSFER_PER_GB = 0.09

def bytes_to_gb(bytes_val):
    """Convert bytes to GB"""
    return bytes_val / (1024 ** 3)

def calculate_storage_cost(image_size_bytes):
    """Calculate ECR storage cost"""
    size_gb = bytes_to_gb(image_size_bytes)
    return size_gb * ECR_STORAGE_PER_GB

def calculate_build_cost(build_minutes=10):
    """Calculate GitHub Actions cost"""
    return build_minutes * GITHUB_ACTIONS_PER_MIN

def calculate_runtime_cost(vcpu=0.25, memory_gb=0.5, hours=730):
    """Calculate Fargate runtime cost"""
    vcpu_cost = vcpu * ECS_FARGATE_PER_VCPU * hours
    memory_cost = memory_gb * ECS_FARGATE_PER_GB * hours
    return vcpu_cost + memory_cost

def calculate_transfer_cost(gb_per_month=10):
    """Calculate data transfer cost"""
    return gb_per_month * DATA_TRANSFER_PER_GB

def main():
    parser = argparse.ArgumentParser(
        description='Calculate deployment cost'
    )
    parser.add_argument(
        '--image-size',
        type=int,
        required=True,
        help='Docker image size in bytes'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region'
    )
    parser.add_argument(
        '--vcpu',
        type=float,
        default=0.25,
        help='vCPU (default: 0.25)'
    )
    parser.add_argument(
        '--memory',
        type=float,
        default=0.5,
        help='Memory GB (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    # Calculate
    storage = calculate_storage_cost(args.image_size)
    build = calculate_build_cost(10)
    runtime = calculate_runtime_cost(args.vcpu, args.memory)
    transfer = calculate_transfer_cost(10)
    
    total = storage + build + runtime + transfer
    
    # Print
    print(f"💰 Deployment Cost Estimate ({args.region})")
    print("=" * 45)
    print(f"ECR Storage:      ${storage:>7.2f}/month")
    print(f"Build (Actions):  ${build:>7.2f}/month")
    print(f"Runtime (Fargate):${runtime:>7.2f}/month")
    print(f"Data Transfer:    ${transfer:>7.2f}/month")
    print("=" * 45)
    print(f"TOTAL:            ${total:>7.2f}/month")
    print()
    
    # Output for GitHub Actions
    print(f"{total:.2f}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())