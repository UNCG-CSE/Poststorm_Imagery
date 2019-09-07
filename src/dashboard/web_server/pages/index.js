import Layout from '../src/components/layout'
import Fetch from 'isomorphic-unfetch';
import { MDBBtn, MDBCard, MDBCardBody, MDBCardImage, MDBCardTitle, MDBCardText, MDBCol } from 'mdbreact';

const Index = (props) => (
    
        <Layout >
          
            <center>
                <MDBCol className="pt-2">
                    <MDBCard style={{ width: "auto" }} className="stylish-color-dark">

                        <MDBCardImage className="w-75 img-fluid pt-4 pb-4 px-2" src={props.file_url} waves />
                    
                        <MDBCardBody >
                            <MDBCardTitle className="white-text h3">{props.file_name}</MDBCardTitle>
                            <MDBCardText className="white-text">
                                <b>
                                    <u>
                                        Wowe api call
                                    </u>
                                </b>

                                <p className='red-text'>
                                {JSON.stringify(props,null,8)}
                                </p>
                            </MDBCardText>
                            <MDBBtn href="register">MDBBtn</MDBBtn>
                        </MDBCardBody>
                    </MDBCard>
                </MDBCol>
            </center>
            
        </Layout>
    
)

Index.getInitialProps = async function() {
    const IP='35.239.226.117'//'192.168.56.1';
    const res = await fetch('http://'+IP+':4000/')
    const data = await res.json()
    return data
}

export default Index;