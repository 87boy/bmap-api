<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Local_search_model extends CI_Model {
    public function __construct() {
        parent::__construct();
    }
    public function insert($data) {
        return $this->db->insert('shanghai', $data);
    }
}