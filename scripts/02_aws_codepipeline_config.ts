// AWS CodePipeline configuration script for DevSecOps
// This script generates CloudFormation/CDK configuration for AWS CI/CD pipeline

const awsCodePipelineConfig = {
  // CodePipeline stages
  pipeline: {
    name: "medical-records-devsecops-pipeline",
    artifactStore: {
      type: "S3",
      location: "${ARTIFACT_BUCKET_NAME}",
    },
    stages: [
      {
        name: "Source",
        actions: [
          {
            name: "SourceAction",
            actionTypeId: {
              category: "Source",
              owner: "GitHub",
              provider: "GitHub",
              version: "1",
            },
            configuration: {
              Owner: "${GITHUB_OWNER}",
              Repo: "${GITHUB_REPO}",
              Branch: "${GITHUB_BRANCH}",
              OAuthToken: "${GITHUB_TOKEN}",
            },
            outputArtifacts: [{ name: "SourceOutput" }],
          },
        ],
      },
      {
        name: "SAST",
        actions: [
          {
            name: "CodeQualityScan",
            actionTypeId: {
              category: "Build",
              owner: "AWS",
              provider: "CodeBuild",
              version: "1",
            },
            configuration: {
              ProjectName: "medical-records-sast-scan",
            },
            inputArtifacts: [{ name: "SourceOutput" }],
            outputArtifacts: [{ name: "SastOutput" }],
          },
        ],
      },
      {
        name: "DependencyCheck",
        actions: [
          {
            name: "VulnerabilityScanning",
            actionTypeId: {
              category: "Build",
              owner: "AWS",
              provider: "CodeBuild",
              version: "1",
            },
            configuration: {
              ProjectName: "medical-records-dependency-scan",
            },
            inputArtifacts: [{ name: "SastOutput" }],
            outputArtifacts: [{ name: "DepCheckOutput" }],
          },
        ],
      },
      {
        name: "SecretsDetection",
        actions: [
          {
            name: "SecretScan",
            actionTypeId: {
              category: "Build",
              owner: "AWS",
              provider: "CodeBuild",
              version: "1",
            },
            configuration: {
              ProjectName: "medical-records-secrets-scan",
            },
            inputArtifacts: [{ name: "DepCheckOutput" }],
            outputArtifacts: [{ name: "SecretsOutput" }],
          },
        ],
      },
      {
        name: "Build",
        actions: [
          {
            name: "BuildAndContainer",
            actionTypeId: {
              category: "Build",
              owner: "AWS",
              provider: "CodeBuild",
              version: "1",
            },
            configuration: {
              ProjectName: "medical-records-build",
            },
            inputArtifacts: [{ name: "SecretsOutput" }],
            outputArtifacts: [{ name: "BuildOutput" }],
          },
        ],
      },
      {
        name: "ContainerScan",
        actions: [
          {
            name: "ECRImageScan",
            actionTypeId: {
              category: "Build",
              owner: "AWS",
              provider: "CodeBuild",
              version: "1",
            },
            configuration: {
              ProjectName: "medical-records-container-scan",
            },
            inputArtifacts: [{ name: "BuildOutput" }],
            outputArtifacts: [{ name: "ContainerScanOutput" }],
          },
        ],
      },
      {
        name: "Deploy",
        actions: [
          {
            name: "DeployToProduction",
            actionTypeId: {
              category: "Deploy",
              owner: "AWS",
              provider: "CloudFormation",
              version: "1",
            },
            configuration: {
              ActionMode: "CHANGE_SET_EXECUTE",
              StackName: "medical-records-prod",
              ChangeSetName: "pipeline-changeset",
              TemplatePath: "BuildOutput::packaged.yaml",
            },
            inputArtifacts: [{ name: "ContainerScanOutput" }],
            runOrder: 1,
          },
        ],
      },
    ],
  },

  // CodeBuild projects
  codeBuildProjects: {
    sast: {
      name: "medical-records-sast-scan",
      serviceRole: "${CODEBUILD_ROLE_ARN}",
      artifacts: { type: "CODEPIPELINE" },
      environment: {
        computeType: "BUILD_GENERAL1_MEDIUM",
        image: "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
        environmentVariables: [
          { name: "SONAR_HOST_URL", value: "${SONAR_HOST_URL}", type: "PARAMETER_STORE" },
          { name: "SONAR_TOKEN", value: "${SONAR_TOKEN}", type: "SECRETS_MANAGER" },
        ],
      },
      source: {
        type: "CODEPIPELINE",
        buildspec: "buildspec-sast.yml",
      },
    },
    dependencyScan: {
      name: "medical-records-dependency-scan",
      serviceRole: "${CODEBUILD_ROLE_ARN}",
      artifacts: { type: "CODEPIPELINE" },
      environment: {
        computeType: "BUILD_GENERAL1_SMALL",
        image: "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
        environmentVariables: [{ name: "SNYK_TOKEN", value: "${SNYK_TOKEN}", type: "SECRETS_MANAGER" }],
      },
      source: {
        type: "CODEPIPELINE",
        buildspec: "buildspec-dependency.yml",
      },
    },
    secretsScan: {
      name: "medical-records-secrets-scan",
      serviceRole: "${CODEBUILD_ROLE_ARN}",
      artifacts: { type: "CODEPIPELINE" },
      environment: {
        computeType: "BUILD_GENERAL1_SMALL",
        image: "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
      },
      source: {
        type: "CODEPIPELINE",
        buildspec: "buildspec-secrets.yml",
      },
    },
    build: {
      name: "medical-records-build",
      serviceRole: "${CODEBUILD_ROLE_ARN}",
      artifacts: { type: "CODEPIPELINE" },
      environment: {
        computeType: "BUILD_GENERAL1_MEDIUM",
        image: "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
        environmentVariables: [
          { name: "ECR_REPOSITORY_URI", value: "${ECR_REPOSITORY_URI}" },
          { name: "IMAGE_TAG", value: "latest" },
        ],
      },
      source: {
        type: "CODEPIPELINE",
        buildspec: "buildspec-build.yml",
      },
    },
    containerScan: {
      name: "medical-records-container-scan",
      serviceRole: "${CODEBUILD_ROLE_ARN}",
      artifacts: { type: "CODEPIPELINE" },
      environment: {
        computeType: "BUILD_GENERAL1_MEDIUM",
        image: "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
        environmentVariables: [{ name: "ECR_REPOSITORY_URI", value: "${ECR_REPOSITORY_URI}" }],
      },
      source: {
        type: "CODEPIPELINE",
        buildspec: "buildspec-container-scan.yml",
      },
    },
  },
}

export default awsCodePipelineConfig
