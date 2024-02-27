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

            train = fe_obj.fit_transform(train)

            test = fe_obj.transform(test)

            train.to_csv(os.path.join(self.config.Transformed_data_path, "train.csv"), index=False, mode='w')
            test.to_csv(os.path.join(self.config.Transformed_data_path, "test.csv"), index=False, mode='w')

            logger.info("Data Saved after feature_engineering")

            processing_obj = self.get_data_transformation_obj()

            traget_columns_name = "CLASS_LABEL"
            
            X_train = train.drop(columns = traget_columns_name, axis = 1)
            y_train = train[traget_columns_name]
            
            X_test = test.drop(columns = traget_columns_name, axis = 1)
            y_test = test[traget_columns_name]
            
            logger.info(X_train.columns)
            X_train = processing_obj.fit_transform(X_train)
            X_test = processing_obj.transform(X_test)
            
            train_arr = np.c_[X_train, np.array(y_train)]
            test_arr = np.c_[X_test, np.array(y_test)]

            df_train = pd.DataFrame(train_arr)
            df_test = pd.DataFrame(test_arr)

            
            df_train.to_csv(os.path.join(self.config.Transformed_data_path, "train.csv"),index = False)
            df_test.to_csv(os.path.join(self.config.Transformed_data_path, "test.csv"),index = False)

            logger.info("Processed and Feature Engineered data")
            logger.info(df_train.shape)
            logger.info(df_test.shape)

            joblib.dump(processing_obj,self.config.Processed_data_OBJ_PATH)

            joblib.dump(fe_obj, self.config.Transformed_data_OBJ_PATH)

            logger.info("Successfully dump {} and, {}".format(self.config.Processed_data_OBJ_PATH,self.config.Processed_data_OBJ_PATH))
            logger.info("Data Transformation completed")
            return(train_arr,
                   test_arr,
                   self.config.Processed_data_OBJ_PATH)

        except Exception as e:
                 error = CustomException(e, sys)
                 logger.info(error.error_message)