class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {page: 'Home',
                  power: 0};
  }
  handlePowerChange = (power) => {
    this.setState({power:power});
  }
  render(){
    if (this.state.page === 'Home'){
      return (
        <div className="text-center">
          <p>HOME PAGE RENDERED</p>
          <button onClick={() => {this.setState({page: 'Program'})}} className="btn btn-primary btn-lg m-1" >Program</button>
          <button onClick={() => {this.setState({page: 'History'})}} className="btn btn-primary btn-lg m-1" >History</button>
          <PowerButton
              power={this.state.power}
              onPowerChange={this.handlePowerChange}
          />
        </div>
      );
    }
    else if (this.state.page === 'Program'){
      return (
        <div className="text-center">
          <p>PROGRAM PAGE RENDERED</p>
          <button onClick={() => {this.setState({page: 'Home'})}} className="btn btn-primary btn-lg m-1" >Exit</button>
        </div>
      );
    }
    else if (this.state.page === 'History'){
      return(
        <div className="text-center">
          <p>HISTORY PAGE RENDERED</p>
          <button onClick={() => {this.setState({page: 'Home'})}} className="btn btn-primary btn-lg m-1" >Exit</button>
        </div>
      );
    }
  }
}

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);
