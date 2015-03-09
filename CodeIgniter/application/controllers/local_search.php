<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Local_search extends CI_Controller {
    public function __construct() {
        parent::__construct();
    }
    public function index() {
        $this->load->view('local_search.html');
    }
    public function insert() {
        $data = $this->input->post();
        //$data = array("status" => "ok");
        //$data = json_encode($data);
        $this->load->model('Local_search_model', 'local_search');
        $result = $this->local_search->insert($data);
        var_dump($result);
        //return is_array($data);
        //var_dump($data);
    }
}