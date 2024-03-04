import os
import sys
import pandas as pd
import joblib
import numpy as np
from CREDIT_UTILITY.logger import logger
from CREDIT_UTILITY.Exception import CustomException
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from CREDIT_UTILITY.entity.config_entity import DataTransformationConfig


class Feature_Engineering(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        logger.info("******************feature Engineering started******************")


    def transform_data(self,data):

        try:

            #data = pd.read_csv(self.config.data_path)
            data.drop('id', axis=1, inplace=True)
            Discrete_features_more_than_2_categories=['NumDots','SubdomainLevel','PathLevel','NumDash',
                                                      'NumDashInHostname','NumUnderscore','NumPercent',
                                                      'NumQueryComponents','NumAmpersand','NumSensitiveWords',
                                                      'SubdomainLevelRT','UrlLengthRT','PctExtResourceUrlsRT',
                                                      'AbnormalExtFormActionR','ExtMetaScriptLinkRT',
                                                      'PctExtNullSelfRedirectHyperlinksRT']
        
            for feature in Discrete_features_more_than_2_categories:
                kmeans = KMeans(n_clusters=4, random_state=42)
                cluster_labels = kmeans.fit_predict(data[[feature]])
                data[feature] = cluster_labels

            logger.info(f"Applying KNN to reduce the Cardinality")
            return(data)
        
        except Exception as e:
                error = CustomException(e, sys)
                logger.info(error.error_message)



    def fit(self,X,y=None):
        return self 
    

    def transform(self,X:pd.DataFrame,y=None):
        try:    
            transformed_df=self.transform_data(X)
            return transformed_df
        
        except Exception as e:
                 error = CustomException(e, sys)
                 logger.info(error.error_message)






class DataTransformation:


    def __init__(self, config: DataTransformationConfig):
        self.config = config


    def get_data_transformation_obj(self):
        
        try:  
            
            
            continuous_features=['UrlLength', 'NumNumericChars', 'HostnameLength', 'PathLength', 'QueryLength',
                                  'PctExtHyperlinks', 'PctExtResourceUrls', 'PctNullSelfRedirectHyperlinks']
            
            Discrete_features=['NumDots','SubdomainLevel','PathLevel','NumDash','NumDashInHostname','AtSymbol','TildeSymbol','NumUnderscore',
                            'NumPercent','NumQueryComponents','NumAmpersand','NumHash','NoHttps','RandomString','IpAddress',
                            'DomainInSubdomains','DomainInPaths','HttpsInHostname','DoubleSlashInPath','NumSensitiveWords','EmbeddedBrandName',
                            'ExtFavicon','InsecureForms','RelativeFormAction','ExtFormAction','AbnormalFormAction','FrequentDomainNameMismatch','FakeLinkInStatusBar',
                            'RightClickDisabled','PopUpWindow','SubmitInfoToEmail','IframeOrFrame','MissingTitle','ImagesOnlyInForm',
                            'SubdomainLevelRT','UrlLengthRT','PctExtResourceUrlsRT','AbnormalExtFormActionR','ExtMetaScriptLinkRT',
                            'PctExtNullSelfRedirectHyperlinksRT']
            
            # Numerical pipeline
            numerical_pipeline = Pipeline(steps = [
                 ('scaler', StandardScaler(with_mean=False))])

            # Categorical Pipeline
            categorical_pipeline = Pipeline(steps = [
                ('onehot', OneHotEncoder(handle_unknown = 'ignore')),
                ('scaler', StandardScaler(with_mean=False))])
            
            preprocssor = ColumnTransformer([
                ('numerical_pipeline', numerical_pipeline,continuous_features ),
                ('categorical_pipeline', categorical_pipeline,Discrete_features )])
            
            logger.info("Pipeline Steps Completed")
            return preprocssor
      
        except Exception as e:
                 error = CustomException(e, sys)
                 logger.info(error.error_message)


    def get_feature_engineering_object(self):
        try:
            feature_engineering = Pipeline(steps = [("fe",Feature_Engineering())])

            return feature_engineering 
        
        except Exception as e:
            error = CustomException(e, sys)
            logger.info(error.error_message)


    def train_test_spliting(self):
        data = pd.read_csv(self.config.data_path)
        
        train, test = train_test_split(data, test_size = 0.20, random_state= 42)
        
        train.to_csv(os.path.join(self.config.Transformed_data_path, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.Transformed_data_path, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)
  

    def inititate_data_transformation(self):
        try:
            train = pd.read_csv(self.config.train_data_path)
            test = pd.read_csv(self.config.test_data_path)

            logger.info("Obtaining FE steps object")
            fe_obj = self.get_feature_engineering_object()

            logger.info("Applying feature engineering on train and test sets")
            train = fe_obj.fit_transform(train)
            test = fe_obj.transform(test)

            train.to_csv("train_data.csv")
            test.to_csv("test_data.csv")

            logger.info("Data Saved after feature_engineering")

            processing_obj = self.get_data_transformation_obj()

            target_column_name = "CLASS_LABEL"

            X_train = train.drop(columns=[target_column_name], axis=1)
            y_train = train[target_column_name]

            X_test = test.drop(columns=[target_column_name], axis=1)
            y_test = test[target_column_name]

            logger.info("Applying data transformation on train and test sets")
            X_train = processing_obj.fit_transform(X_train)
            X_test = processing_obj.transform(X_test)

            # Get transformed column names
            transformed_columns = []
            for name, transformer, features in processing_obj.transformers_:
                if hasattr(transformer, 'get_feature_names_out'):
                    if hasattr(transformer, 'categories_'):
                        transformed_columns.extend(transformer.get_feature_names_out())
                    else:
                        transformed_columns.extend(transformer.get_feature_names_out(features))
                else:
                    transformed_columns.extend(features)

            # Save transformed arrays with column names
            np.savetxt(os.path.join(self.config.Transformed_data_path, "X_train.csv"), X_train, delimiter=",", header=",".join(transformed_columns))
            np.savetxt(os.path.join(self.config.Transformed_data_path, "X_test.csv"), X_test, delimiter=",", header=",".join(transformed_columns))
            np.savetxt(os.path.join(self.config.Transformed_data_path, "y_train.csv"), y_train, delimiter=",", header=target_column_name)
            np.savetxt(os.path.join(self.config.Transformed_data_path, "y_test.csv"), y_test, delimiter=",", header=target_column_name)

            logger.info("Processed and Feature Engineered data")
            logger.info("X_train shape: {}".format(X_train.shape))
            logger.info("X_test shape: {}".format(X_test.shape))

            joblib.dump(processing_obj, self.config.Processed_data_OBJ_PATH)
            joblib.dump(fe_obj, self.config.Transformed_data_OBJ_PATH)

            logger.info("Successfully dumped {} and, {}".format(self.config.Processed_data_OBJ_PATH, self.config.Processed_data_OBJ_PATH))
            logger.info("Data Transformation completed")
            return (X_train, y_train), (X_test, y_test), self.config.Processed_data_OBJ_PATH

        except Exception as e:
            error = CustomException(e, sys)
            logger.info(error.error_message)